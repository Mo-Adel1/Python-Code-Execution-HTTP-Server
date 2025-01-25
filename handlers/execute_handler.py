import json
from server.responses import build_http_response
from execution.python_executor import run_user_code

def handle_execute_route(method, body):
    if method != "POST":
        return build_http_response(405, {"error": "Method Not Allowed"})
    
    is_valid, result = validate_and_parse_request(body)
    if not is_valid:
        return result
    
    try:
        execution_result = run_user_code(result)
        return format_execution_response(execution_result)
    except Exception:
        return build_http_response(500, {"error": "Internal server error"})

def validate_and_parse_request(body):
    body_json = parse_json(body)
    if not body_json and body_json != {}:
        return False, build_http_response(400, {"error": "Invalid JSON payload"})
    
    extra_keys = [key for key in body_json.keys() if key != "code"]
    if extra_keys:
        return False, build_http_response(400, {"error": f"Unexpected keys: {', '.join(extra_keys)}"})

    code = body_json.get("code")
    if not code or not code.strip():
        return False, build_http_response(400, {"error": "Code is required"})
    
    return True, code

def parse_json(body):
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def format_execution_response(execution_result):
    stdout, stderr = execution_result.get("stdout"), execution_result.get("stderr")
    if execution_result.get("error"):
        return build_http_response(500, {"error": execution_result.get("error")})
    if stdout and stderr:
        return build_http_response(200, {"stdout": stdout, "stderr": stderr})
    elif stdout:
        return build_http_response(200, {"stdout": stdout})
    elif stderr:
        return build_http_response(200, {"stderr": stderr})
    return build_http_response(200, {"stdout": "", "stderr": ""})
