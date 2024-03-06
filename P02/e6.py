from client0 import Client
from Seq1 import Seq
import os
import socket

PRACTICE = 2
EXERCISE = 5
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 10


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip_1 = "255.255.224.0"
port_1 = 2024
ip_2 = "255.255.224.0"
port_2 = 2025


c = Client(ip_1, port_1)
l = Client(ip_2, port_2)

filename = os.path.join("..", "sequences", Gene)
s = Seq()
s.read_fasta(filename)
print(f"Gene {Gene},  {s}")
gene_sequence = str(s)

for g in range(NUMBER_OF_FRAGMENTS):
    start_index = g * 10
    end_index = start_index + 10
    fragment = gene_sequence[start_index: end_index]
    print(f"Fragment {g + 1}: {fragment} ")

    if g / 2 == 0:
        response = c.talk(gene_sequence)
    elif g / 2 != 0:
        response = l.talk(gene_sequence)







