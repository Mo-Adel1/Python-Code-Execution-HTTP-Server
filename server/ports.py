import socket
from .user_prompts import prompt_for_port, handle_no_available_ports

def handle(host, port):
    """
    Checks if the given port is available.
    If the port is taken, it either finds a new one or prompts the user.
    """
    if is_port_available(host, port):
        return port

    print(f"Error: Port {port} is already in use.")
    
    available_port = find_available_port(host)
    if available_port:
        chosen_port = prompt_for_port(available_port)
        if chosen_port:
            return chosen_port
        else:
            print("Exiting the server...")
            exit()
    else:
        return handle_no_available_ports()

def is_port_available(host, port):
    """
    Checks if the port is available by attempting to bind a socket to it.
    Returns True if available, False if taken.
    """
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test_socket.bind((host, port))
        test_socket.close()
        return True
    except OSError:
        return False
    
def find_available_port(host, start_port=8766, end_port=8800):
    """
    Finds an available port by checking the range from start_port to end_port.
    """
    for port in range(start_port, end_port + 1):
        if is_port_available(host, port):
            return port
    return None
