from client0 import Client
from Seq1 import Seq
import os

PRACTICE = 2
EXERCISE = 4
Genes = ["ADA.txt", "U5.txt", "FRAT1.txt"]

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.33" #servidor laptop dulce
PORT = 8081

c = Client(IP, PORT)
s = Seq()
for g in Genes:
    filename = os.path.join("..", "sequences", g)
    s = Seq()
    s.read_fasta(filename)

    msg = f"Sending {g} Gene to the server..."
    print(f"To server: {msg}")
    response = c.talk(msg)
    print(f"From server: {response}")


    msg = str(s)
    print(f"To server: {msg}")
    response = c.talk(msg)
    print(f"From server: {response}")
