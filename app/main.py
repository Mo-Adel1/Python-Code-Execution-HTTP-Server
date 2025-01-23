from server import HTTPServer

def main():
    server = HTTPServer(host='localhost', port=8765)
    server.start()

if __name__ == "__main__":
    main()