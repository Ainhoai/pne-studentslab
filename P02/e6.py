from client0 import Client
from Seq1 import Seq
import os

PRACTICE = 2
EXERCISE = 6
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 10
NUMBER_OF_BASES = 10

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip = "127.0.0.1"
port_1 = 8080
port_2 = 8081

c1 = Client(ip, port_1)
print(c1)
c2 = Client(ip, port_2)
print(c2)

filename = os.path.join("..", "sequences", Gene)

s = Seq()
s.read_fasta(filename)
print(f"Gene {Gene},  {s}")
msg = f"Sending {Gene} gene to the server, in fragments of {NUMBER_OF_BASES} bases..."
c1.talk(msg)
c2.talk(msg)

for g in range(NUMBER_OF_FRAGMENTS):
    start = 0
    end = NUMBER_OF_BASES
    fragments = str(s)[start:end]
    msg = f"Fragment {g + 1}: {fragments}"
    print(msg)
    if g % 2 != 1:
        c1.talk(msg)
    else:
        c2.talk(msg)

    start += NUMBER_OF_BASES
    end += NUMBER_OF_BASES






