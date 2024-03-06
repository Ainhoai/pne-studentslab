import socket


PORT = 8081
IP = "127.0.0.1"  #this is my ip

MAX_OPEN_REQUESTS = 5
number_con = 0
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print(f"Waiting for connections at {IP}, {PORT} ")
        (client_socket, address) = serversocket.accept()
        number_con += 1
        print(f"CONNECTION: {number_con}. From the address: {address}")
        msg = client_socket.recv(2048).decode("utf-8")
        print(f"Message from client: {msg}")
        message = "Hello from the teacher's server\n"
        send_bytes = str.encode(message)
        client_socket.send(send_bytes)
        client_socket.close()
except socket.error:
    print(f"Problems using ip {IP} port {PORT}. Is the IP correct? Do you have port permission?")
except KeyboardInterrupt:
    print("Server stopped by the user")
    serversocket.close()
