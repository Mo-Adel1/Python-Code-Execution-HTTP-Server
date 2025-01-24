import socket
from .responses import build_http_response

class HTTPServer:
    host = 'localhost'
    port = 8765
    routes = {}
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def register_route(self, path, handler):
        self.routes[path] = handler

    def start(self):
        print(f"Starting server...")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Server running at http://{self.host}:{self.port}")

        while True:
            connection, client_address = server_socket.accept()
            self.handle_request(connection, client_address)

    def handle_request(self, connection, client_address):
        request = connection.recv(1024).decode('utf-8')

        if not request:
            connection.close()
            return
        
        method, path, http_version, headers, body = self.parse_http_request(request)

        print(f"Request from: {client_address}")
        print(f"{method} {path} {http_version}")
        
        handler = self.routes.get(path)
        if handler:
            response = handler(method, body)
        else:
            response = build_http_response(404, {"error": f"'{path}' path not found"})
        connection.sendall(response.encode('utf-8'))
        connection.close()

    def parse_http_request(self, request):
        lines = request.split('\r\n')
        method, path, http_version = lines[0].split()
        headers = {}
        for line in lines[1:]:
            if line == "":
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        body = ""
        if "\r\n\r\n" in request:
            body = request.split("\r\n\r\n")[1]

        return method, path, http_version, headers, body
