def format_response(output):
    session_id = output.get("id")
    stdout = output.get("stdout")
    stderr = output.get("stderr")
    err = output.get("error")

    response = {"id": session_id}  # Include the session ID in the response
    if err:
        response["error"] = err
        return (500, response)
    else:
        if stdout:
            response["stdout"] = stdout
        if stderr:
            response["stderr"] = stderr
        return (200, response)