import socket
from .ports import handle

def initialize_server(host, port):
    port = handle(host, port)
    if port is None:
        raise ValueError("No available port found!")
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"--> listening on http://{host}:{port}")
    print("(*) Press Ctrl+C to stop the server.")
    
    return server_socket
