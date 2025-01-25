from .socket import initialize_server
from .process import process

class HTTPServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.routes = {}

    def register_route(self, path, handler):
        self.routes[path] = handler

    def start(self):
        print(f"Starting server...")

        server = initialize_server(self.host, self.port)

        while True and server != None:
            process(server, self.routes)

