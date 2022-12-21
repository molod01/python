#!C:\Program Files\Python310\python.exe
import os
import base64
import mysql.connector
import dao
from db import db_conf
# Authorization Server


def send401(message: str = None) -> None:
    print("Status: 401 Unauthorized")
    print('WWW-Authenticate: Basic realm "Authorization required" ')
    print()
    if message:

        print(message)
    return


# дістаємо заголовок Authorization
if 'HTTP_AUTHORIZATION' in os.environ.keys():
    auth_header = os.environ['HTTP_AUTHORIZATION']

else:
    # відправляємо 401
    send401()
    exit()

# Перевіряємо схему авторизації - має бути Basic
if auth_header.startswith('Basic'):
    credentials = auth_header[6:]
else:
    send401("Authorization scheme Basic required")
    exit()
# декодуємо credentials
try:
    data = base64.b64decode(credentials, validate=True).decode('utf-8')
except:
    send401("Credentials invalid: Base64 string required")
    exit()

if not ":" in data:
    send401("Credentials invalid: Login:Password format excepted")
    exit()

login, password = data.split(":", maxsplit=1)

try:
    db = mysql.connector.connect(**db_conf)
except mysql.connector.Error as err:
    send401(err)
    exit()

user_dao = dao.UserDAO(db)

user = user_dao.read_auth(login, password)

if not user:
    send401("Credentials rejected")
    exit()

# Успішне завершення
print("Status: 200 OK")
print("Content-Type: text/plain")
print()
print(f'''
{{
    "access_token":"{user.id},
    "token_type":"Bearer",
    "expires_in":3600
}} ''', end="")
