import io
import json
import sys
from response import create_response
def execute_handler(method, path, headers, body):
    if method == "POST":
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
            return json.dumps({"stdout": stdout.getvalue()})
        if stderr:
            return json.dumps({"stderr": "error"})
        
        return json.dumps({"error": "error"})
    else:
        return json.dumps({"error": "Invaild request method"})