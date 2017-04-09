from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import base64
import json
from datetime import timedelta
from datetime import datetime
from configparser import ConfigParser

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    client_id = config['team16']['ClientId']
    client_secret = config['team16']['ClientSecret']

    return (client_id, client_secret)

class CoreHandler(BaseHTTPRequestHandler):
    _bearer_token = None
    _bearer_token_expires = datetime.min

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Hello world!\n')

        #bearer_token = self.bearer_token(client_id, client_secret)
        #self.wfile.write(bytes(bearer_token + '\n', 'utf-8'))
        search1 = self.search('Danger Zone')
        self.wfile.write(bytes(str(search1), 'utf-8'))
        self.wfile.write(b'\n')

    def bearer_token(self, client_id, client_secret):
        if self._bearer_token is None:
            # Get the auth value and encode it in base 64.
            client_id_secret = base64.b64encode(bytes('{}:{}'.format(client_id, client_secret), 'utf-8')).decode('utf-8')

            auth_request = requests.post(
                'https://accounts.spotify.com/api/token',
                headers={
                    'Authorization': 'Basic {}'.format(client_id_secret),
                    'Content-Type': 'application/x-www-form-urlencoded'},
                    data='grant_type=client_credentials')
            auth = json.loads(auth_request.content)

            self._bearer_token = auth['access_token']
            self._bearer_token_expires = datetime.utcnow() + timedelta(seconds=auth['expires_in'])
            print('Successfully acquired application bearer token. Expires at {}'
                .format(self._bearer_token_expires))
            
        return self._bearer_token

    def search(self, term):
        client_id, client_secret = read_config()

        search_request = requests.get(
            'https://api.spotify.com/v1/search',
            params={'q': term, 'type': 'track', 'limit': 5},
            headers={
                'Authorization': 'Bearer {}'.format(self.bearer_token(client_id, client_secret))
            })
        search_results = json.loads(search_request.content)

        return search_results

def run_server():
    server_address = ('localhost', 8888)
    httpd = HTTPServer(server_address, CoreHandler)
    httpd.serve_forever()

run_server()

