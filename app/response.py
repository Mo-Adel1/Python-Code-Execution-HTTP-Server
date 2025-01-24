import json

def response(status_code, message, content_type="application/json"):
    status_messages = {
        200: "OK",
        404: "Not Found",
        400: "Bad Request",
        405: "Method Not Allowed",
        500: "Internal server error",
    }
    status_message = status_messages.get(status_code, "OK")
    
    if isinstance(message, dict):
        message = json.dumps(message)
    
    response_line = f"HTTP/1.1 {status_code} {status_message}\r\n"
    headers = f"Content-Type: {content_type}\r\nContent-Length: {len(message)}\r\n\r\n"
    
    return response_line + headers + message
