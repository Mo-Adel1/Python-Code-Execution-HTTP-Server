import json
from response import response
from executor import execute_user_code

def execute_handler(method, path, headers, body):
    if method != "POST":
        return response(405, {"error": "Method Not Allowed"})
    
    is_valid, result = parse_request_body(body)
    if not is_valid:
        return result
    
    try:
        execution_result = execute_user_code(result)
        return build_response(execution_result)
    except Exception:
        return response(500, {"error": "Internal server error"})

def parse_request_body(body):
    """Parses and validates the request body."""
    if not body:
        return False, response(400, {"error": "Empty body is not allowed"})
    
    body_json = parse_json(body)
    if not body_json:
        return False, response(400, {"error": "Invalid JSON payload"})
    
    extra_keys = [key for key in body_json.keys() if key != "code"]
    if extra_keys:
        return False, response(400, {"error": f"Unexpected keys: {', '.join(extra_keys)}"})

    code = body_json.get("code")
    if not code or not code.strip():
        return False, response(400, {"error": "Code is required"})
    
    return True, code

def parse_json(body):
    """Safely parse JSON from the request body."""
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def build_response(execution_result):
    """Builds a structured response based on execution result."""
    stdout, stderr = execution_result.get("stdout"), execution_result.get("stderr")
    if stdout and stderr:
        return response(200, {"stdout": stdout, "stderr": stderr})
    elif stdout:
        return response(200, {"stdout": stdout})
    elif stderr:
        return response(200, {"stderr": stderr})
    return response(500, {"error": "Internal server error"})
