import socket

class HTTPServer:
    host = 'localhost'
    port = 8765
    def __init__(self, host, port: int):
        self.host = host
        self.port = port
    
    def start(self):
        print(f"Starting server...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running at http://{self.host}:{self.port}")
        connection, client_address = server_socket.accept()
        self.handle_incomming_request(connection, client_address)

    def handle_incomming_request(self, connection, client_address):
        request = connection.recv(1024).decode('utf-8')
        print("Handling request...")
        print(f"connection: {request}")
        print(f"Request from: {client_address[0]}")
        method, path, http_version, headers, body = self.parse_request(request)
        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"HTTP Version: {http_version}")
        print(f"Headers: {headers}")
        print(f"Body: {body}")
        

    def parse_request(self, request):
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
        

    def create_response(self, request):
        pass