import socket

class HTTPServer:
    host = 'localhost'
    port = 8765
    def __init__(self, host, port: int):
        self.host = host
        self.port = port
    
    def start(self):
        pass

    def handle_request(self, request):
        pass

    def parse_request(self, request):
        pass

    def create_response(self, request):
        pass