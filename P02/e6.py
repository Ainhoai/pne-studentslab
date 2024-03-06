from client0 import Client
from Seq1 import Seq
import os
import socket

PRACTICE = 2
EXERCISE = 5
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 10


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

ip_1 = ""
port_1 = 2024
ip_2 = ""
port_2 = 2025


c1 = Client(ip_1, port_1)
c2 = Client(ip_2, port_2)

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
    response = c1.talk(gene_sequence)
elif g / 2 != 0:
    response = c2.talk(gene_sequence)







