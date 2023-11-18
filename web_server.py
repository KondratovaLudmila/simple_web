from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_to_bytes
from pathlib import Path
import mimetypes
from udp_socket import send_to_udp_server, UDPSocketServer
from threading import Event

HOST = ""
PORT = 3000
HTML = {"": "index.html",
        "home": "index.html",
        "message": "message.html",
        "error": "error.html"}

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path[1:]
        file_name = HTML.get(path)
        if file_name:
            self.send_html_file(file_name)
        elif Path().joinpath(path).exists():
            self.send_static()
        else:
            self.send_html_file(HTML.get("error"), 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = unquote_to_bytes(data)
        send_to_udp_server(data_parse)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, file_name, status: int=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(file_name, 'rb') as fd:
            self.wfile.write(fd.read())
        
    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

class WebServer(HTTPServer):
    def serve_forever(self, poll_interval: float = 0.5, event: Event=None) -> None:
        if event:
            while not event.is_set():
                self.handle_request()
        else:
            return super().serve_forever(poll_interval)
    
def run_server(event: Event=None, server_class=WebServer, handler_class=HTTPRequestHandler):
    server_address = (HOST, PORT)
    server = server_class(server_address, handler_class)
    server.serve_forever(event=event)
    server.server_close()


