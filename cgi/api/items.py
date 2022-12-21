#!C:\Program Files\Python310\python.exe
import os
import mysql.connector
import dao
from db import db_conf

# API demo - доступ до ресурсу обмеженого доступу (Resource Server)
# дістаємо заголовок Authorization


def send401(message: str = None):
    print("Status: 401 Unauthorized")
    print("WWW-Authenticate: Basic realm :Authorization required")
    print()
    if message:
        print(message)
    return


if 'HTTP_AUTHORIZATION' in os.environ.keys():
    auth_header = os.environ['HTTP_AUTHORIZATION']
else:
    send401()
    exit()

try:
    db = mysql.connector.connect(**db_conf)
except mysql.connector.Error as err:
    send401(err)
    exit()

# user_dao = dao.UserDAO(db)

# if auth_header.startswith('Bearer') and \
#         (auth_header[7:] in [user.id for user in user_dao.read()]):
#     token = auth_header[7:]
# else:
#     send401()
#     exit()

# Успішне завершення
print("Status: 200 OK")
print("Content-Type: text/plain;")
print()
print(f'"{db_conf}"')
