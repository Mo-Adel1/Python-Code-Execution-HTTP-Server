import json

def parse_json(body):
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None

def validate_body(body):
    expected_keys = {"code", "id"}
    unexpected_keys = set(body.keys()) - expected_keys
    if unexpected_keys:
        return False, (400, {"error": f"Unexpected key(s): {', '.join(unexpected_keys)}"})

    code = body.get("code")
    if not code or not code.strip():
        return False, (400, {"error": "Code is required"})
    
    return True, None

def extract_body(body):
    code = body.get("code")
    session_id = body.get("id")
    return {"code": code, "id": session_id}