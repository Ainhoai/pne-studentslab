
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8081

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

guessed = False
while not guessed:
    try:
        n = int(input("Please, enter a valid number:  "))
        request = str(n)
        request_bytes = request.encode("utf-8")
        client_socket.send(request_bytes)

        response_bytes = client_socket.recv(2048)
        response = response_bytes.decode("utf-8")
        if response == "Lower" or response == "Higher":
            print(response)
        else:
            print(response)
            guessed = True

    except ValueError:
        print("Please enter a valid number.")
client_socket.close()

