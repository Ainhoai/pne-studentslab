from client0 import Client
PRACTICE = 3
EXERCISE = 7

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")


SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
N = 5
SEQUENCE = "ACCTCCTCTCCAGCAATGCCAACCCCAGTCCAGGCCCCCATCCGCCCAGGATCTCGATCA"
GENES = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P"]

c = Client(SERVER_IP, SERVER_PORT)
print(f"* Testing PING...")
response = c.talk("PING")
print(response)

print(f"* Testing GET...")
for n in range(N): #N: constante creada previamente; n: index.
    response = c.talk(f"GET {n}")
    print(f"GET: {response}")

print(f"* Testing INFO...")
print(f"INFO {SEQUENCE}")
response = c.talk(f"INFO {SEQUENCE}")
print(response)

print(f"* Testing COMP...")
print(f"COMP {SEQUENCE}")
response = c.talk(f"COMP {SEQUENCE}")
print(response)

print(f"* Testing REV...")
print(f"REV {SEQUENCE}")
response = c.talk(f"REV {SEQUENCE}")
print(response)

print(f"* Testing GENE...")
for g in GENES:
    print(f"GENE {GENES}")
    response = c.talk(f"GENE {GENES}")
    print(response)









