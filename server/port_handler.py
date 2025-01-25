import socket
from .user_prompts import prompt_for_port, handle_no_available_ports

def handle_port_conflicts(host, port):

    if is_port_available(host, port):
        return port

    print(f"Error: Port {port} is already in use.")
    
    available_port = find_available_port(host)
    if available_port:
        return prompt_for_port(available_port)
    else:
        return handle_no_available_ports()


def is_port_available(host, port):
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test_socket.bind((host, port))
        test_socket.close()
        return True
    except OSError:
        return False
    
def find_available_port(host, start_port=8766, end_port=8800):
    for port in range(start_port, end_port + 1):
        if is_port_available(host, port):
            return port
    return None