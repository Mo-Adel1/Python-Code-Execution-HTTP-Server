def create_response(status_code, body, content_type="text/html"):
    status_messages = {200: "OK", 404: "Not Found", 400: "Bad Request", 405: "Method Not Allowed"}
    status_message = status_messages.get(status_code, "OK")
    response_line = f"HTTP/1.1 {status_code} {status_message}\r\n"
    headers = f"Content-Type: {content_type}\r\nContent-Length: {len(body)}\r\n\r\n"
    return response_line + headers + body
