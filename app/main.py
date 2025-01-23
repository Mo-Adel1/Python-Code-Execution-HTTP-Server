from server import HTTPServer
from routes import execute_handler
def main():
    server = HTTPServer(host='localhost', port=8765)
    server.add_route("/execute", execute_handler)
    server.start()

if __name__ == "__main__":
    main()