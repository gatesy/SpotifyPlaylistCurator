import http.server
import json

class TrackRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)

        requested_tracks = json.loads(data)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        for track in requested_tracks:
            print('{}'.format(track['id']))

