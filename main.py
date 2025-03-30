import socket
import threading
import tkinter as tk
from datetime import datetime

class Router:
    def __init__(self):
        self.routes = {}
        self.methods = {}

    def setpath(self, client, path, methods=["GET"]):
        def wrapper(func):
            self.routes[path] = func
            self.methods[path] = methods
            return func
        return wrapper

    def get_route(self, path):
        return self.routes.get(path, None)

    def get_methods(self, path):
        return self.methods.get(path, ["GET"])

class VSPEXHOST:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.router = Router()
        self.logs = {"Errors": [], "Messages": [], "Requests": [], "Welcome": []}
        self.gui_initialized = False

    def log_action(self, section, action):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{action} - {timestamp}"
        self.logs[section].append(log_entry)
        if self.gui_initialized:
            self.update_gui()

    def make(self, render, html, code, client, application):
        if render == "html":
            return self.render_html(code)
        return code

    def render_html(self, content):
        return f"<html><body>{content}</body></html>"

    def handle_request(self, client_socket):
        request_data = client_socket.recv(1024).decode('utf-8')
        if request_data:
            first_line = request_data.split("\n")[0]
            path = first_line.split(" ")[1]
            method = first_line.split(" ")[0]
            self.log_action("Requests", f"Received {method} request for {path}")
            route_func = self.router.get_route(path)
            allowed_methods = self.router.get_methods(path)
            if route_func and method in allowed_methods:
                response_code = 'HTTP/1.1 200 OK'
                content = route_func()
                self.log_action("Requests", f"Route {path} found, responding with 200 OK")
            else:
                response_code = 'HTTP/1.1 404 Not Found'
                content = self.make("render", "html", "<h1>404 Not Found</h1>", client_socket, self)
                self.log_action("Errors", f"Route {path} not found, responding with 404 Not Found")
            response = f"{response_code}\r\nContent-Type: text/html\r\n\r\n{content}"
            client_socket.sendall(response.encode('utf-8'))
        client_socket.close()

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            self.log_action("Messages", f"Server started at http://{self.host}:{self.port}")
            self.gui_initialized = True
            self.update_gui()
            while True:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=self.handle_request, args=(client_socket,)).start()

    def initialize_gui(self):
        self.root = tk.Tk()
        self.root.title("VSPEXHOST Server Logs")
        self.textbox = tk.Text(self.root, height=20, width=80)
        self.textbox.pack()
        self.gui_initialized = True

    def update_gui(self):
        if self.gui_initialized:
            self.textbox.delete(1.0, tk.END)
            for section, logs in self.logs.items():
                self.textbox.insert(tk.END, f"\n{section}:\n")
                for log in logs:
                    self.textbox.insert(tk.END, log + '\n')
            self.root.update_idletasks()
            self.root.update()

    def run_gui(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = VSPEXHOST(host='localhost', port=8081)  # Changed port to 8081 to avoid conflicts

    @app.router.setpath(client=None, path='/')
    def home():
        return app.make("render", "html", "<h1>Welcome to VSPEXHOST!</h1><p>This is the home page.</p>", None, app)

    @app.router.setpath(client=None, path='/about')
    def about():
        return app.make("render", "html", "<h1>About VSPEXHOST</h1><p>This is a simple Python web server.</p>", None, app)

    app.log_action("Welcome", "Welcome to VspexHost!")
    app.log_action("Welcome", "Made by Xscripts Inc.")
    app.log_action("Welcome", "Enjoy!")
    app.log_action("Welcome", "Feel free to explore the server and its features.")
    app.log_action("Welcome", "This is a simple and lightweight server.")
    app.log_action("Welcome", "It can handle basic web requests with Python.")
    app.log_action("Welcome", "Have fun while learning how web servers work in Python!")
    app.log_action("Welcome", "The server is fully customizable for any need!")
    app.log_action("Welcome", "New features will be added over time.")
    app.log_action("Welcome", "Thank you for using VspexHost!")

    app.initialize_gui()
    
    # Start the server in a separate thread
    threading.Thread(target=app.start, daemon=True).start()

    # Run the GUI in the main thread
    app.run_gui()

