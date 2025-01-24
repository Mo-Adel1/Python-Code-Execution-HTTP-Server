import json
import sys
import io
import re
import traceback
from response import response

def execute_handler(method, path, headers, body):
    if method != "POST":
        return response(405, {"error": "Method Not Allowed"})
    
    is_valid, result = parse_request_body(body)
    if not is_valid:
        return result  # Return the error response directly
    
    code = result  # This is the valid code to execute

    try:
        execution_result = execute_user_code(code)
        
        # Determine if stdout or stderr should be returned
        if execution_result["stderr"] and execution_result["stdout"]:
            return response(200, execution_result)
        elif execution_result["stdout"]:
            return response(200, {"stdout": execution_result.get("stdout", "")})
        else:
            return response(200, {"stderr": execution_result.get("stderr", "")})
    
    except Exception:
        return response(500, {"error": "Internal server error"})

def parse_request_body(body):
    if not body:  # Check if body is empty
        return False, response(400, {"error": "Empty body is not allowed"})
    
    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        return False, response(400, {"error": "Invalid JSON payload"})
    
    # Validate 'code' key in the JSON body
    if "code" not in body_json:
        return False, response(400, {"error": "'code' key is required"})

    if not body_json.get("code").strip():
        return False, response(400, {"error": "No code to execute"})
    
    return True, body_json.get("code")

def execute_user_code(code):
    stdout = io.StringIO()
    stderr = io.StringIO()

    # Redirect standard output and error
    sys.stdout = stdout
    sys.stderr = stderr

    try:
        exec(code, {})
        return {"stdout": stdout.getvalue(), "stderr": ""}
    except Exception:
        raw_traceback = traceback.format_exc()
        clean_traceback = clean_traceback_paths(raw_traceback)
        return {"stdout": stdout.getvalue(), "stderr": clean_traceback}
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def clean_traceback_paths(traceback_str):
    # Replace all file paths with "<stdin>"
    cleaned_traceback = re.sub(r'File ".*?",', 'File "<stdin>",', traceback_str)

    # Remove the internal exec and line references to keep only relevant traceback lines
    cleaned_traceback = re.sub(r'  File "<stdin>", line \d+, in .*\n    .*\n    ~+.*\n', '', cleaned_traceback)

    # Remove extra leading spaces and unnecessary internal lines
    cleaned_lines = []
    capture = False

    for line in cleaned_traceback.splitlines():
        if "File \"<stdin>\"," in line:
            capture = True
        if capture:
            cleaned_lines.append(line)
    
    # Add the traceback header manually if it's not already included
    if "Traceback (most recent call last):" not in cleaned_lines:
        cleaned_lines.insert(0, "Traceback (most recent call last):")

    # Return the cleaned traceback
    return "\n".join(cleaned_lines)
