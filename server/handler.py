def handle_request(connection):
    try:
        raw_request = connection.recv(1024).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to read request: {e}")

    if not raw_request.strip():
        raise ValueError("Empty request received")

    request_lines = raw_request.split('\r\n')
    try:
        method, path, http_version = request_lines[0].split()
    except ValueError:
        raise ValueError("Malformed request line")

    headers = {}
    body = None
    line_iter = iter(request_lines[1:])
    for line in line_iter:
        if line == "":
            body = "\r\n".join(line_iter)
            break
        try:
            key, value = line.split(": ", 1)
            headers[key] = value
        except ValueError:
            raise ValueError(f"Malformed header line: {line}")

    return method, path, http_version, headers, body
