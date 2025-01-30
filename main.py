from routes import controller
from server.core import HTTPServer
# import cProfile

def main():
    server = HTTPServer('localhost', 8765)
    server.register_route("/execute", controller.handler)
    server.start()

if __name__ == "__main__":
    main()
    # cProfile.run('main()', 'profile_output.prof')