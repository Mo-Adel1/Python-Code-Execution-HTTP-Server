import socket

def initialize_server(host, port):
    port = handle_port_conflicts(host, port)
    if port is None:
        print("Server could not be started. Exiting...")
        return
    
    print(f"Server running at http://{host}:{port}")

    server_socket = get_socket_server(host, port)
    return server_socket


def handle_port_conflicts(host, port):
    if is_port_available(host, port):
        return port

    print(f"Error: Port {port} is already in use.")
    available_port = find_available_port(host)
    if available_port:
        return prompt_for_port(available_port)
    else:
        return handle_no_available_ports()


def prompt_for_port(available_port):
    print(f"Available port: {available_port}")
    use_new_port = input(f"Would you like to use port {available_port}? (y/n): ")
    return available_port if use_new_port.lower() == 'y' else None


def handle_no_available_ports():
    print("No available ports found.")
    retry = input("Would you like to try again later? (y/n): ")
    if retry.lower() == 'y':
        print("Retrying in a few seconds...")
    return None


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


def get_socket_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    return server_socket
