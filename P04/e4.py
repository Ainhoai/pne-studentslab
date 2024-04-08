import socket
import termcolor
from pathlib import Path
import os

IP = "127.0.0.1"
PORT = 8080


def process_client(client_socket):
    request_bytes = client_socket.recv(2048)
    request = request_bytes.decode()
    lines = request.splitlines()
    request_line = lines[0]
    print("Request line: ", end="")
    termcolor.cprint(request_line, 'green')
    slices = request_line.split(' ')
    method = slices[0]
    resource = slices[1]
    version = slices[2]

    if resource == "/info/A":
        file_name = os.path.join("html", "A.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    elif resource == "/info/C":
        file_name = os.path.join("html", "C.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    elif resource == "/info/G":
        file_name = os.path.join("html", "G.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    elif resource == "/info/T":
        file_name = os.path.join("html", "T.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 200 OK\n"
    else:
        file_name = os.path.join("html", "index.html")
        body = Path(file_name).read_text()
        status_line = "HTTP/1.1 404 Not_found\n"
    header = "Content-Type: text/html\n"
    header += f"Content-Length: {len(body)}\n"
    response = f"{status_line}{header}\n{body}"
    response_bytes = response.encode()
    client_socket.send(response_bytes)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

print("DNA Bases Server configured!")

try:
    while True:
        print("Waiting for clients...")

        (client_socket, client_address) = server_socket.accept()
        process_client(client_socket)
        client_socket.close()
except KeyboardInterrupt:
    print("Server Stopped!")
    server_socket.close()
