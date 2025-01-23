import json
def execute_handler(method, path, headers, body):
    if method == "POST":
        return json.dumps({"stdout": "done"})
    else:
        return json.dumps({"error": "Invaild request method"})