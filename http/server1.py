import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
import os


class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        path_parts = self.path.split('/')
        if path_parts[1] == "":
            path_parts[1] = "index.html"
        fname = './http/' + path_parts[1]
        if os.path.isfile(fname):
            self.flush_file(fname)
            return
        if path_parts[1] == 'auth':
            self.auth()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write('<h1>Hello</h1>'.encode())
        return

    def flush_file(self, filename):
        extension = filename[filename.rindex('.'):]
        if extension == 'ico':
            content_type = 'image/x-icon'
        elif extension in ('html', 'htm'):
            content_type = 'text/html'
        else:
            content_type = 'aplication/octet-stream'
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open(filename, "rb") as f:
            self.wfile.write(f.read())
        return

    def auth(self):
        auth_header = self.headers.get("Authorization")
        if not auth_header:
            self.send401("Authorization header required")
            return
        if auth_header.startswith('Basic '):
            credentials = auth_header[6:]
        else:
            self.send401('Authorization scheme Basic required')
            return
        try:
            data = base64.b64decode(credentials, validate=True).decode('utf-8')
        except:
            self.send401('Credentials invalid: Base64 string required')
            return

    def send401(message: str = None) -> None:
        print("Status: 401 Unauthorized")
        print('WWW-Authenticate: Basic realm "Authorization required" ')
        print()
        if message:
            print(message)
        return


def main():
    http_server = HTTPServer(('127.0.0.1', 88), MainHandler)
    try:
        print("Server started")
        http_server.serve_forever()
    except:
        print('Server stopped')


if __name__ == "__main__":
    main()
