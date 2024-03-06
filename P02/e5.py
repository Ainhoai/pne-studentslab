from client0 import Client
from Seq1 import Seq
import os

PRACTICE = 2
EXERCISE = 5
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 5
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.0.30" #servidor laptop prof
PORT = 8081

c = Client(IP, PORT)

filename = os.path.join("..", "sequences", Gene)
s = Seq()
s.read_fasta(filename)
print(f"Gene {Gene},  {s}")

for g in range(1, NUMBER_OF_FRAGMENTS + 1):
    print(f"Fragment: ")