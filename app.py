from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import base64
import json
from datetime import timedelta
from datetime import datetime
from configparser import ConfigParser
import oauth

def read_config():
    config = ConfigParser()
    config.read('config.ini')
    client_id = config['team16']['ClientId']
    client_secret = config['team16']['ClientSecret']

    return (client_id, client_secret)

def create_client_credentials():
    client_id, client_secret = read_config()
    return oauth.ClientCredentials(client_id, client_secret)

class CoreHandler(BaseHTTPRequestHandler):

    client_credentials = create_client_credentials()

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

    def search(self, term):
        search_request = requests.get(
            'https://api.spotify.com/v1/search',
            params={'q': term, 'type': 'track', 'limit': 5},
            headers={'Authorization': 'Bearer {}'.format(self.client_credentials.get_token())})
        search_results = json.loads(search_request.content)

        return search_results

def run_server():
    server_address = ('localhost', 8888)
    httpd = HTTPServer(server_address, CoreHandler)
    httpd.serve_forever()

run_server()

