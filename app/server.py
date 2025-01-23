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
        print("Handling request...")
        print(f"connection: {connection}")
        print(f"Request from: {client_address}")

    def parse_request(self, request):
        pass

    def create_response(self, request):
        pass