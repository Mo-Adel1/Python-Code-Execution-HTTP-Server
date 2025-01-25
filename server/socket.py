import socket
from .port_handler import handle_port_conflicts

def initialize_server(host, port):
    port = handle_port_conflicts(host, port)

    if port is None:
        print("Server could not be started. Exiting...")
        return
    
    server_socket = get_socket_server(host, port)

    print(f"Server running at http://{host}:{port}")

    return server_socket

def get_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))
    server_socket.listen()

    return server_socket
