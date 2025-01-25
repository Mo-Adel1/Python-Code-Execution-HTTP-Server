from .requests import handle_request
from .responses import http_response
def process(server_socket, routes):
    connection, client_address = server_socket.accept()

    method, path, http_version, headers, body = handle_request(connection, client_address)

    response = map_route(routes, method, path, body)
    
    connection.sendall(response.encode('utf-8'))
    connection.close()

def map_route(routes, method, path, body):
    handler = routes.get(path)
    if handler:
        status_code, message = handler(method, body)
        return http_response(status_code, message)
    else:
        return http_response(404, {"error": f"'{path}' path not found"})
