import socket

class HTTPServer:
    host = 'localhost'
    port = 8765
    routes = {}
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def add_route(self, path, handler):
        self.routes[path] = handler

    def start(self):
        print(f"Starting server...")

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)

        print(f"Server running at http://{self.host}:{self.port}")

        while True:
            connection, client_address = server_socket.accept()
            self.handle_incomming_request(connection, client_address)

    def handle_incomming_request(self, connection, client_address):
        request = connection.recv(1024).decode('utf-8')
        if not request:
            connection.close()
            return
        
        method, path, http_version, headers, body = self.parse_request(request)

        print(f"Request from: {client_address}")
        print(f"{method} {path} {http_version}")
        
        handler = self.routes.get(path)
        result_executed_code = {}
        if handler:
            result_executed_code = handler(method, path, headers, body)
        
        response = self.create_response(200, result_executed_code)
        
        connection.sendall(response.encode('utf-8'))
        connection.close()

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
        

    def create_response(self, status_code, result_executed_code):
        status_messages = {200: "OK", 404: "Not Found", 400: "Bad Request", 405: "Method Not Allowed"}
        status_message = status_messages.get(status_code, "OK")
        response_line = f"HTTP/1.1 {200} {status_message}\r\n"
        headers = f"Content-Type: {"text/html"}\r\nContent-Length: {len(result_executed_code)}\r\n\r\n"
        return response_line + headers + result_executed_code

    def execute_code(self, code):
        pass