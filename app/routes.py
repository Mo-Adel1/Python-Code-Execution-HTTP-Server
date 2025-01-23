import json
from response import create_response
def execute_handler(method, path, headers, body):
    if method == "POST":
        body = json.loads(headers["body"])
        code = body.get("code")
        if not code:
            return create_response(400, json.dumps({"error": "Missing 'code' field"}), content_type="application/json")

        return json.dumps({"stdout": "done"})
    else:
        return json.dumps({"error": "Invaild request method"})