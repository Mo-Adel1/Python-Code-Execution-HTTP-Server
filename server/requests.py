def handle_request(connection, client_address):
    request = connection.recv(1024).decode('utf-8')
    if not request:
        connection.close()
        return
    
    lines = request.split('\r\n')
    method, path, http_version = lines[0].split()
    headers = {}
    for line in lines[1:]:
        if line == "":
            break
        key, value = line.split(": ", 1)
        headers[key] = value
    body = ""
    if "\r\n\r\n" in request:
        body = request.split("\r\n\r\n")[1]
    
    print(f"Request from: {client_address}")
    print(f"{method} {path} {http_version}")

    return method, path, http_version, headers, body
