#!C:\Program Files\Python39\python.exe
import os
import sys
import base64

content_length = 0

cred = "admin:123"
cred_bytes = cred.encode('utf-8')
code_bytes = base64.b64encode(cred_bytes)
code_str = code_bytes.decode('ascii')

content_length += len(code_str) + 1

method = os.environ["REQUEST_METHOD"]

content_length += len(method) + 1

query = os.environ["QUERY_STRING"]
if len(query):
    content_length += len(query) + 1
    params = dict()
    for param in query.split('&'):
        param = param.split('=')
        params[param[0]] = param[1]
    content_length += len(str(params)) + 1

headers = {}
for k, v in os.environ.items():
    if k.startswith("HTTP_"):
        headers[k[5:].lower()] = v

k = "CONTENT_LENGTH"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]
k = "CONTENT_TYPE"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]

content_length += len(str(headers)) + 1

body = sys.stdin.read()

content_length += len(body)

print("Connection: close")
print(f"Content-Length: {content_length}")
print()
print(method)
if len(query):
    print(query)
    print(params)
print(headers)
if len(body):
    print(body)
print(code_str)
