from server.http_server import HTTPServer
from handlers.execute_handler import handle_execute_route
def main():
    server = HTTPServer()
    server.register_route("/execute", handle_execute_route)
    server.start()

if __name__ == "__main__":
    main()