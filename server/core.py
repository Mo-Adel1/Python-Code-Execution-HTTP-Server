import signal
import threading
from .process import process
from .socket_utils import initialize_server
from multiprocessing import active_children


class HTTPServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.routes = {}
        self.is_running = False
        self.server_socket = None
        self.server_thread = None
        self.stop_event = threading.Event()

    def register_route(self, path, handler):
        if not callable(handler):
            raise ValueError("Handler must be callable")
        self.routes[path] = handler

    def start(self):
        print("Starting server...")
        with initialize_server(self.host, self.port) as server_socket:
            self.server_socket = server_socket
            self.is_running = True
            self.server_thread = threading.Thread(target=self.run_server, daemon=True)
            self.server_thread.start()

            signal.signal(signal.SIGINT, self.stop)

            try:
                while self.is_running:
                    self.stop_event.wait(timeout=0.1)
            except KeyboardInterrupt:
                self.stop()

    def run_server(self):
        while self.is_running:
            try:
                self.server_socket.settimeout(1.0)
                process(self.server_socket, self.routes)
            except Exception as e:
                print(f"Error during server operation: {e}", exc_info=True)
                break

    def stop(self, signum=None, frame=None):
        print("Shutting down the server...")
        self.is_running = False
        self.stop_event.set()
        if self.server_socket:
            self.server_socket.close()
        for child in active_children():
            child.terminate()
        print("Server stopped.")
