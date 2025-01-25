import json
from execution import python

def handler(method, body):
    
    if method != "POST":
        return (405, {"error": "Method Not Allowed"})
    
    is_valid, result = validate_and_parse_request(body)
    if not is_valid:
        return result
    
    try:
        execution_result = python.run(result)
        return format_execution_response(execution_result)
    except Exception:
        return (500, {"error": "Internal server error"})

def validate_and_parse_request(body):
    body_json = parse_json(body)
    if not body_json and body_json != {}:
        return False, (400, {"error": "Invalid JSON payload"})
    
    extra_keys = [key for key in body_json.keys() if key != "code"]
    if extra_keys:
        return False, (400, {"error": f"Unexpected keys: {', '.join(extra_keys)}"})

    code = body_json.get("code")
    if not code or not code.strip():
        return False, (400, {"error": "Code is required"})
    
    return True, code

def parse_json(body):
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def format_execution_response(execution_result):
    stdout, stderr = execution_result.get("stdout"), execution_result.get("stderr")
    if execution_result.get("error"):
        return (500, {"error": execution_result.get("error")})
    if stdout and stderr:
        return (200, {"stdout": stdout, "stderr": stderr})
    elif stdout:
        return (200, {"stdout": stdout})
    elif stderr:
        return (200, {"stderr": stderr})
    return (200, {"stdout": "", "stderr": ""})
