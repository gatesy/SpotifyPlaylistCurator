import http.server
import requests
import json
import oauth
import urllib.parse
import re
import search

class RoutingHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, handlers):
        self.handlers = handlers
        super().__init__(request, client_address, server)

    def __getattribute__(self, name):
        if(name.startswith('do_')):
            handler_class = self.get_handler_class()
            if(handler_class is not None):
                # disable the 'handle' method
                handler_class.handle = lambda *args: None
                # instantiate the handler
                handler = handler_class(self.request, self.client_address, self.server)
                # copy all of our properties into it.
                handler.__dict__.update(self.__dict__)
                # return the handler's do_* method
                return handler.__getattribute__(name)
            else:
                return self.not_found
        return object.__getattribute__(self, name)

    def get_handler_class(self):
        parsed_url = urllib.parse.urlparse(self.path)
        for path_and_handler in self.handlers:
            if re.search(path_and_handler[0], parsed_url.path):
                return path_and_handler[1]
        return None

    def not_found(self):
        self.send_error(404)

class DefaultHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Spotify Playlist Curator API\n')

def handler_factory(handlers):
    return lambda request, client_address, server: RoutingHandler(request, client_address, server, handlers)

def run_server():

    handlers = [
        ('^/search$', search.SearchHandler),
        ('^/$', DefaultHandler)
    ]

    server_address = ('localhost', 8888)
    httpd = http.server.HTTPServer(server_address, handler_factory(handlers))
    httpd.serve_forever()

run_server()

