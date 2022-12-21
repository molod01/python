#!C:\Program Files\Python310\python.exe

html = '''<!DOCTYPE html>
<html>
    <head>
    <head/>
    <body>
        <h1>Hello World</h1>
    <body/>
<html/>
'''

print("Content-Type: text/html")
print(f"Content-Length: {len(html)}")
print()
print(html)
