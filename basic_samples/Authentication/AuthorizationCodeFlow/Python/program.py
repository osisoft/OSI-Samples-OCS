import base64
import configparser
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import secrets
from selenium import webdriver
import time
from urllib.parse import urlparse, parse_qs
import webbrowser


def main(test=False):
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')

        resource = config.get('Configuration', 'Resource')
        tenantId = config.get('Configuration', 'TenantId')
        clientId = config.get('Configuration', 'ClientId')

        redirectUri = 'http://localhost:5004/callback.html'
        scope = 'openid ocsapi'

        # Set up PKCE Verifier and Code Challenge
        verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)).rstrip(b'=')
        challenge = base64.urlsafe_b64encode(
            hashlib.sha256(verifier).digest()).rstrip(b'=')

        # Get OAuth endpoint configuration
        print()
        print('Step 1: Get OAuth endpoint configuration...')
        endpoint = json.loads(requests.get(
            resource + '/identity/.well-known/openid-configuration').content)
        authEndpoint = endpoint.get('authorization_endpoint')
        tokenEndpoint = endpoint.get('token_endpoint')

        # Set up request handler for web browser login
        print()
        print('Step 2: Set up server to process authorization response...')

        class RequestHandler(BaseHTTPRequestHandler):
            code = ''

            def do_GET(self):
                # Parse out authorization code from query string in request
                RequestHandler.code = parse_qs(
                    urlparse(self.path).query)['code'][0]

                # Write response
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    '<h1>You can now return to the application.</h1>'.encode())
                return

        # Set up server for web browser login
        server = HTTPServer(('', 5004), RequestHandler)

        # Open web browser against authorization endpoint
        print()
        print('Step 3: Authorize the user...')
        authUrl = authEndpoint + \
            '?response_type=code&code_challenge=' + challenge.decode() + \
            '&code_challenge_method=S256&client_id=' + clientId + \
            '&redirect_uri=' + redirectUri + \
            '&scope=' + scope + \
            '&acr_values=tenant:' + tenantId

        if test == True:
            # Get Config
            username = config.get('Test', 'Username')
            password = config.get('Test', 'Password')

            # Open Chrome Webdriver, go to Auth page
            print()
            print('Selenium 1: Open Chrome WebDriver')
            browser = webdriver.Chrome()
            browser.get(authUrl)
            time.sleep(2)

            # Use Personal Account (Must be enabled on Tenant)
            print()
            print('Selenium 2: Choose Personal Account')
            browser.find_element_by_xpath(
                xpath='descendant::a[@title="Personal Account"]').click()
            time.sleep(2)

            # Enter Username and submit
            print()
            print('Selenium 3: Enter Username')
            browser.find_element_by_xpath(
                '//*[@id="i0116"]').send_keys(username)
            browser.find_element_by_xpath('//*[@id="idSIButton9"]').click()
            time.sleep(2)

            # Enter Password and submit
            print()
            print('Selenium 4: Enter Password')
            browser.find_element_by_xpath(
                '//*[@id="i0118"]').send_keys(password)
            elem = browser.find_element_by_xpath('//*[@id="idSIButton9"]')
            try:
                browser.set_page_load_timeout(2)
                elem.click()
            except Exception:
                print('Ignore time out, start the server...')
        else:
            # Open user default web browser at Auth page
            webbrowser.open(authUrl)

        # Wait for response in browser
        print()
        print('Step 4: Set server to handle one request...')
        server.handle_request()

        # Use authorization code to get bearer token
        print()
        print('Step 5: Get a token using the authorization code...')
        token = requests.post(tokenEndpoint, [
                              ('grant_type', 'authorization_code'),
                              ('client_id', clientId),
                              ('code_verifier', verifier),
                              ('code', RequestHandler.code),
                              ('redirect_uri', redirectUri)])

        token = json.loads(token.content).get('access_token')
        print()
        print('Step 6: Read the Access Token:')
        print(token)

        if test == True:
            assert token, "Failed to obtain access token"

        print()
        print('Complete!')
    except Exception as e:
        print()
        msg = "Encountered Error: {error}".format(error=e)
        print(msg)
        assert False, msg


if __name__ == "__main__":
    main()
