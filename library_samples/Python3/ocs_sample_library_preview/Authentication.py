
from .SdsError import SdsError

import base64
import configparser
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os 
import secrets
import time
from urllib.parse import urlparse, parse_qs
import webbrowser

import requests


class Authentication(object):

    def __init__(self, tenant, url, clientId, clientSecret):
        self.__tenant = tenant
        self.__clientId = clientId
        self.__clientSecret = clientSecret
        self.__url = url

        self.__expiration = 0
        self.__token = ""
        if clientSecret is not None:
            self.__getToken = self.__getClientIDSecretToken
        else:
            self.__getToken = self.__getPKCEToken
        

    def getToken(self):
        if ((self.__expiration - time.time()) > 5 * 60):
            return self.__token

        return self.__getToken()


    def __getClientIDSecretToken(self):
        tokenEndpoint = self.__url + "/identity/connect/token"

        tokenInformation = requests.post(
            tokenEndpoint,
            data={"client_id": self.__clientId,
                  "client_secret": self.__clientSecret,
                  "grant_type": "client_credentials"})

        token = json.loads(tokenInformation.content)

        expiration = token.get("expires_in", None)
        if expiration is None:
            raise SdsError(
                f"Failed to get token, check client id/secret: {token['error']}")

        self.__expiration = float(expiration) + time.time()
        self.__token = token['access_token']
        return self.__token

    def __getPKCEToken(self):
        try:
            redirect_uri = 'http://localhost:5004/callback.html'
            scope = 'openid ocsapi'

            # Set up PKCE Verifier and Code Challenge
            verifier = base64.urlsafe_b64encode(
                secrets.token_bytes(32)).rstrip(b'=')
            challenge = base64.urlsafe_b64encode(
                hashlib.sha256(verifier).digest()).rstrip(b'=')

            # Get OAuth endpoint configuration
            print('Step 1: Get OAuth endpoint configuration...')
            endpoint = json.loads(requests.get(
                self.__url + '/identity/.well-known/openid-configuration').content)
            auth_endpoint = endpoint.get('authorization_endpoint')
            token_endpoint = endpoint.get('token_endpoint')

            # Set up request handler for web browser login
            print('Step 2: Set up server to process authorization response...')

            class RequestHandler(BaseHTTPRequestHandler):
                """Handles authentication redirect uri and extracts authorization code from URL"""
                code = ''

                # pylint: disable=C0103
                def do_GET(self):
                    """Handles GET request against this temporary local server"""
                    # Parse out authorization code from query string in request
                    RequestHandler.code = parse_qs(
                        urlparse(self.path).query)['code'][0]

                    # Write response
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html')
                    self.end_headers()
                    self.wfile.write(
                        '<h1>You can now return to the application.</h1>'.encode())

            # Set up server for web browser login
            server = HTTPServer(('', 5004), RequestHandler)

            # Open web browser against authorization endpoint
            print('Step 3: Authorize the user...')
            auth_url = auth_endpoint + \
                '?response_type=code&code_challenge=' + challenge.decode() + \
                '&code_challenge_method=S256&client_id=' + self.__clientId + \
                '&redirect_uri=' + redirect_uri + \
                '&scope=' + scope + \
                '&acr_values=tenant:' + self.__tenant

            # Open user default web browser at Auth page
            if not webbrowser.open(auth_url):
                raise SdsError("This notebook/script should be run locally on your machine to authenticate")

            # Wait for response in browser
            print('Step 4: Set server to handle one request...')
            server.handle_request()

            # Use authorization code to get bearer token
            print('Step 5: Get a token using the authorization code...')
            token = requests.post(token_endpoint, [
                ('grant_type', 'authorization_code'),
                ('client_id', self.__clientId),
                ('code_verifier', verifier),
                ('code', RequestHandler.code),
                ('redirect_uri', redirect_uri)])

            token = json.loads(token.content)  
            expiration = token.get("expires_in", None)
            if expiration is None:
                raise SdsError(f"Failed to get token, please retry login in: {token['error']}")

            self.__expiration = float(expiration) + time.time()
            self.__token = token['access_token']
            print(f"Step 6: Access token read ok\nComplete!")
            return self.__token

        except Exception as error:
            msg = "Encountered Error: {error}".format(error=error)
            raise SdsError(msg)
