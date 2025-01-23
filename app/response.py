def create_response(self, status_code, result_executed_code):
    status_messages = {200: "OK", 404: "Not Found", 400: "Bad Request", 405: "Method Not Allowed"}
    status_message = status_messages.get(status_code, "OK")
    response_line = f"HTTP/1.1 {200} {status_message}\r\n"
    headers = f"Content-Type: {"text/html"}\r\nContent-Length: {len(result_executed_code)}\r\n\r\n"
    return response_line + headers + result_executed_code
