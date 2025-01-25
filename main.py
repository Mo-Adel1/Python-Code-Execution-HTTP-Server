from routes import execute
from server.core import HTTPServer
import sys
import os

# Add project directory to PYTHONPATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
def main():
    server = HTTPServer()
    server.register_route("/execute", execute.handler)
    server.start()

if __name__ == "__main__":
    main()