from routes import execute
from server.core import HTTPServer

def main():
    server = HTTPServer()
    server.register_route("/execute", execute.handler)
    server.start()

if __name__ == "__main__":
    main()