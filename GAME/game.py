
import socket
import random
class Numberguesser:

    MIN = 1
    MAX = 100

    def __init__(self):
        self.secret_number = random.randint(Numberguesser.MIN, Numberguesser.MAX)
        self.attempts = []
        self.guessed = False

    def __str__(self):
        return f"Secret number: {self.secret_number} - Attempt: {self.attempts}"

    def guess(self, number):
        self.attempts.append(number)
        if number < self.secret_number:
            print(f"Higher")
        elif number > self.secret_number:
            print(f"Lower")
        else:
            self.guessed = True
            return f"You won after {len(self.attempts)} attempts."
        return "Well guessed"

    def is_guessed(self):
        return self.guessed

server_port = 8081
server_ip = "127.0.0.1"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print("Guess the number server configured!")

    while True:
        print(f"Waiting for connections at {server_ip}, {server_port}... ")
        (client_socket, address) = server_socket.accept()

        nu = Numberguesser()
        guessed = False
        while not guessed:
            request_bytes = client_socket.recv(2048)
            request = request_bytes.decode("utf-8")
            n = int(request)

            response = nu.guess(n)
            response_bytes = response.encode("utf-8")
            client_socket.send(response_bytes)

            print(nu)
            if nu.is_guessed():
                guessed = True
        client_socket.close()

except socket.error as e:
    print(f"Communication error: {e}")
except KeyboardInterrupt:
    print("Server stopped by the user")
    server_socket.close()



