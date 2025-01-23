import io
import json
import sys
from response import create_response
def execute_handler(method, path, headers, body):
    if method == "POST":
        try:
            body = json.loads(body)
            code = body.get("code")
            if not code:
                return create_response(400, json.dumps({"error": "Missing 'code' field"}), content_type="application/json")

            stdout = io.StringIO()
            stderr = io.StringIO()
            sys.stdout = stdout
            sys.stderr = stderr

            exec(code, {})

            if stdout:
                return create_response(200, json.dumps({"stdout": stdout.getvalue()}), content_type="application/json") 
            if stderr:
                return json.dumps({"stderr": "error"})

            return json.dumps({"error": "error"})
        
        except json.JSONDecodeError:
            return create_response(400, json.dumps({"error": "Invalid JSON payload"}), content_type="application/json")

        except Exception as e:
            return create_response(500, json.dumps({"error": "Internal server error"}), content_type="application/json")

    else:
        return create_response(405, json.dumps({"error": "Method Not Allowed"}), content_type="application/json")
