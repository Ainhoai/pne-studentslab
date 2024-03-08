import socket
import termcolor

IP = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((IP, PORT))
    server_socket.listen()

    print("SEQ Server configure.")

    while True:
        print(f"Waiting for clients ({IP}:{PORT})...")
        (client_socket, client_address) = server_socket.accept()

        request_bytes = client_socket.recv(2048)
        request = request_bytes.decode("utf-8")


        slices = request.split(" ")
        command = slices[0]
        if command == "PING":
            response = "Ok!\n"
        print(response)
        response_bytes = response.encode()
        client_socket.send(response_bytes)



        client_socket.close()

except socket.error:
    print(f"Problems using port {PORT}. Do you have permission?")
except KeyboardInterrupt:
    print("Server stopped by the admin")
    server_socket.close()