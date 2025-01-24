import json
import sys
import io
import traceback
from response import create_response

def execute_handler(method, path, headers, body):
    if method == "POST":
        try:
            body = json.loads(body)
            code = body.get("code")

            if not code:
                return create_response(400, json.dumps({"error": "Missing 'code' field"}), content_type="application/json")

            result = execute_user_code(code)
            if "error" in result:
                return create_response(400, json.dumps({"error": result["error"]}), content_type="application/json")
            elif result["stderr"] and result["stdout"]:
                return create_response(200, json.dumps({"stdout": result.get("stdout", ""), "stderr": result["stderr"]}), content_type="application/json")
            elif result["stderr"]:
                return create_response(200, json.dumps({"stderr": result["stderr"]}), content_type="application/json")
            else:
                return create_response(200, json.dumps({"stdout": result.get("stdout", "")}), content_type="application/json")
        except json.JSONDecodeError:
            return create_response(400, json.dumps({"error": "Invalid JSON payload"}), content_type="application/json")

        except Exception as e:
            return create_response(500, json.dumps({"error": "Internal server error"}), content_type="application/json")

    else:
        return create_response(405, json.dumps({"error": "Method Not Allowed"}), content_type="application/json")

def execute_user_code(code):
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr
    
    try:
        exec(code, {})
        return {"stdout": stdout.getvalue(), "stderr": ""}
    except Exception:
        if stdout.getvalue:
            return {"stdout": stdout.getvalue(), "stderr": traceback.format_exc()}
        return {"stderr": traceback.format_exc(), "stdout": ""}
