import base64
import configparser
import hashlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import requests
import secrets
from urllib.parse import urlparse, parse_qs
import webbrowser

config = configparser.ConfigParser()
config.read('config.ini')

resource = config.get('Configuration', 'Resource')
tenantId = config.get('Configuration', 'TenantId')
clientId = config.get('Configuration', 'ClientId')

redirectUri = 'http://localhost:5004/callback.html'
scope = 'openid ocsapi'

# Set up PKCE Verifier and Code Challenge
verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=')
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
        RequestHandler.code = parse_qs(urlparse(self.path).query)['code'][0]

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
webbrowser.open(authEndpoint +
                '?response_type=code&code_challenge=' + challenge.decode() +
                '&code_challenge_method=S256&client_id=' + clientId +
                '&redirect_uri=' + redirectUri +
                '&scope=' + scope +
                '&acr_values=tenant:' + tenantId)

# Wait for response in browser
server.handle_request()


# Use authorization code to get bearer token
print()
print('Step 4: Get a token using the authorization code...')
token = requests.post(tokenEndpoint, [
                      ('grant_type', 'authorization_code'),
                      ('client_id', clientId),
                      ('code_verifier', verifier),
                      ('code', RequestHandler.code),
                      ('redirect_uri', redirectUri)])

token = json.loads(token.content).get('access_token')
print()
print('Step 5: Read the Access Token:')
print(token)

print()
print('Complete!')
