import datetime
import json
import mysql
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64
import sys
sys.path.append("../cgi/api")
import dao
import db


class DatabaseService:
    __connection = None

    def get_connection(self) -> mysql.connector.MySQLConnection:
        if DatabaseService.__connection\
                or DatabaseService.__connection\
                and DatabaseService.__connection.is_connected():
            return DatabaseService.__connection

        try:
            DatabaseService.__connection = mysql.connector.connect(**db.DB)
        except mysql.connector.Error as error:
            print(error.msg)
            DatabaseService.__connection = None
        return DatabaseService.__connection


class DAOService:
    __user_dao: dao.UserDAO = None
    __access_token_dao: dao.AccessTokenDAO = None
    __database_service: DatabaseService = None

    def __init__(self, database_service):
        DAOService.__database_service = database_service

    def get_user_dao(self) -> dao.UserDAO:
        if DAOService.__user_dao:
            return DAOService.__user_dao
        DAOService.__user_dao = dao.UserDAO(
            DAOService.__database_service.get_connection()
        )
        return DAOService.__user_dao

    def get_access_token_dao(self) -> dao.AccessTokenDAO:
        if DAOService.__access_token_dao:
            return DAOService.__access_token_dao
        DAOService.__access_token_dao = dao.AccessTokenDAO(
            DAOService.__database_service.get_connection()
        )
        return DAOService.__access_token_dao


dao_service: DAOService = None


class MainHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)

        filename = './'
        if self.path == '/':
            filename = "".join([filename, "index.html"])
        else:
            filename = "".join([filename, self.path[self.path.index("/") + 1:]])
        if os.path.isfile(filename):
            self.flush_file(filename)
            return

        if self.path == '/auth':
            self.auth()
        elif self.path == '/items':
            self.items()
        else:
            self.send404()
        return

    EXTENSION_TO_TYPE = {
        "ico": "image/x-icon",
        "html": "text/html",
        "htm": "text/html",
        "js": "application/javascript",
        "css": "text/css"
    }

    def flush_file(self, filename: str):
        extension = filename[filename.rindex(".") + 1:]
        try:
            content_type = self.EXTENSION_TO_TYPE[extension]
        except:
            content_type = "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.end_headers()
        with open(filename, "rb") as file:
            self.wfile.write(file.read())
        return

    def auth(self):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.send_401("Authorization header required")
            return

        if auth_header.startswith("Basic "):
            credentials = auth_header[6:]
        else:
            self.send_401("Authorization scheme Basic required")
            return

        try:
            data = base64.b64decode(credentials, validate=True).decode('utf-8')
        except:
            self.send_401("Invalid credentials: Base64 string required")
            return

        if not ':' in data:
            self.send_401("Invalid credentials: login:password format expected")
            return

        login, password = data.split(':', maxsplit=1)
        user_dao = dao_service.get_user_dao()
        user = user_dao.read_auth(login, password)
        if user is None:
            self.send_401("Credentials rejected")
            return

        access_token_dao = dao_service.get_access_token_dao()
        access_token = access_token_dao.read(user.id)
        if access_token:
            token_expired = (access_token.expires - datetime.now()).seconds < 600
            if token_expired:
                access_token = access_token_dao.create(user)
        else:
            access_token = access_token_dao.create(user)

        if not access_token:
            self.send_401("Token creation error")
            return

        self.send_200(
            json.dumps(access_token.__dict__, indent=4, default=str),
            type="json"
        )
        return

    def items(self):
        auth_header = self.headers.get("Authorization")
        if auth_header is None:
            self.send_401("Authorization header required")
            return

        if auth_header.startswith('Bearer'):
            token = auth_header[7:]
        else:
            self.send_401("Authorization scheme Bearer required")
            return

        access_token_dao = dao_service.get_access_token_dao()

        token = access_token_dao.read(token)
        if not token:
            self.send_401("Token rejected")
            return

        user_list = "<ul>"
        user_dao = dao_service.get_user_dao()
        for user in user_dao.read():
            user_list += f"<li>{user.login} - {user.email}</li>"
        user_list += "</ul>"

        self.send_200(user_list, "html")
        return

    def send_401(self, message=None):
        self.send_response(401, "Unauthorized")
        if message:
            self.send_header("Content-Type", "text/plain")
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def send_200(self, message=None, type="text"):
        self.send_response(200)
        if type == "json":
            content_type = "application/json"
        elif type == "html":
            content_type = "text/html"
        else:
            content_type = "text/plain"

        self.send_header("Content-Type", f"{content_type}; charset=UTF-8")
        self.end_headers()
        if message:
            self.wfile.write(message.encode())
        return

    def send_404(self):
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("<h1>404</h1>".encode())


def main():
    global dao_service
    http_server = HTTPServer(('127.0.0.1', 88), MainHandler)
    try:
        print("Server started")
        dao_service = DAOService(DatabaseService())
        http_server.serve_forever()
    except:
        print('Server stopped')


if __name__ == "__main__":
    main()
