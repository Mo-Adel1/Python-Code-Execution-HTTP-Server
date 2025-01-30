from .response import http_response

def map_route(routes, method, path, body):
    handler = routes.get(path)
    if handler:
        status_code, message = handler(method, body)
        return http_response(status_code, message)
    else:
        return http_response(404, {"error": f"'{path}' path not found"})
