from execution import start
from .response_utils import format_response
from .json_utils import parse_json, validate_body, extract_body

def handler(method, body):
    if method != "POST":
        return (405, {"error": "Method Not Allowed"})
    
    parsed_body = parse_json(body)
    if parsed_body is None or not isinstance(parsed_body, dict):
        return (400, {"error": "Invalid JSON payload"})
    
    is_valid, error_response = validate_body(parsed_body)
    if not is_valid:
        return error_response

    extracted_body = extract_body(parsed_body)
    session_id = extracted_body.get("id")

    try:
        output = start.run(extracted_body['code'], session_id)
        return format_response(output)
    except Exception as e:
        return (500, {"error": "Internal server error"})
