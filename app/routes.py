import json
def execute_handler(method, path, headers, body):
    return json.dumps({"stdout": "done"})
