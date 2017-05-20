import oauth
import requests
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class SearchHandler(BaseHTTPRequestHandler):
    client_credentials = oauth.create_client_credentials()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        search_result = self.search(params['term'])

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        self.wfile.write(search_result)

    def search(self, term):
        search_request = requests.get(
            'https://api.spotify.com/v1/search',
            params={'q': term, 'type': 'track', 'limit': 5},
            headers={'Authorization': 'Bearer {}'.format(self.client_credentials.get_token())})
        return search_request.content
