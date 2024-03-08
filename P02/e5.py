from client0 import Client
from Seq1 import Seq
import os

PRACTICE = 2
EXERCISE = 5
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 5
NUMBER_OF_BASES = 10


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "127.0.0.1"
PORT = 8081

c = Client(IP, PORT)

filename = os.path.join("..", "sequences", Gene)

s = Seq()
s.read_fasta(filename)
print(f"Gene {Gene},  {s}")
c.talk(f"Sending {Gene} gene to the server, in fragments of {NUMBER_OF_BASES} bases...")

for g in range(NUMBER_OF_FRAGMENTS):
    start = 0
    end = NUMBER_OF_BASES
    fragments = str(s)[start:end]
    msg = f"Fragment {g + 1}: {fragments} "
    print(msg)
    c.talk(msg)
    start += NUMBER_OF_BASES
    end += NUMBER_OF_BASES

