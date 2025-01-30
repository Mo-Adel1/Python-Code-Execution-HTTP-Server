from .handler import handle_request
from .routes import map_route

def process(server_socket, routes):
    try:
        connection, client_address = server_socket.accept()

        method, path, http_version, headers, body = handle_request(connection)

        response = map_route(routes, method, path, body)

        connection.sendall(response.encode('utf-8'))
        connection.close()
    except (OSError, ValueError):
        pass
