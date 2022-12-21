#!C:\Program Files\Python310\python.exe

import os
import sys

# метод запиту
method = os.environ["REQUEST_METHOD"]

# заголовки запиту (у lower case)
headers = {}
for k, v in os.environ.items():
    if k.startswith("HTTP_"):
        headers[k[5:].lower()] = v
# окремі заголовки проходять власними назвами:
k = "CONTENT_LENGTH"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]
k = "CONTENT_TYPE"
if k in os.environ.keys():
    headers[k.lower()] = os.environ[k]


# тіло запиту
body = sys.stdin.read()

# URL-параметри (query string)
query = os.environ["QUERY_STRING"]


print("Connection: close")
print("Content-Type: text/plain; charset=cp1251")
print("")
print(method)
print(query)
print(headers)
print(body)

# '''
# API - інтерфейс взаємодії частин програми (комплексу) між собою
#  протиставляється до людинно-машинної взаємодії
# Web-API (Backend-Fronted взаємодія) -> взаємодія за допомогою
#  веб-протоколу НТТР.
# Особливості Web-API:
#  Канали передачі інформації:
#   - метод запиту - рядок, з якого починається запит.
#      Є стандартні методи та методи користувача
#   - URL-параметри (query string)
#   - заголовки - пари "ключ: значення; атрибути"
#   - тіло - довільний контент, відокремлений від заголовків
#       порожнім рядком
# Завдання: вивести всі заголовки запиту
# Підхід: заголовки запиту перетворюються у змінні оточення, імена яких
#  складаються з префіксу НТТР_ та імені заголовку у верхньому реєстрі
#  окремі заголовки проходять власними назвами: CONTENT_LENGTH, CONTENT_TYPE
#  окремі заголовки взагалі не проходять, перехоплюються сервером: Authorization
#    для їх передачі у скрипт потрібно змінювати vhost.conf: додати
#    SetEnvIf Authorization "(.+)" HTTP_AUTHORIZATION=$1
#
# Завдання: вивести тіло запиту
# Підхід: тіло запиту передається у sys.stdin
#
# Завдання: розібрати URL параметри
# Підхід: ці параметри збираються у змінну QUERY_STRING
#
# '''
