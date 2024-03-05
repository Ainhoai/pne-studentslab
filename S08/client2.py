import socket

SERVER_PORT = 8081
SERVER_IP = "127.0.0.1"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((SERVER_IP, SERVER_PORT))

s.send(str.encode("HELLO FROM THE CLIENT!!!"))

msg = s.recv(2048)
print("MESSAGE FROM THE SERVER:\n")
print(msg.decode("utf-8"))

s.close()