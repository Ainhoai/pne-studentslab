from client0 import Client
from Seq1 import Seq
import os

PRACTICE = 2
EXERCISE = 5
Gene = "FRAT1.txt"
NUMBER_OF_FRAGMENTS = 5


print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = ""
PORT = 8081

c = Client(IP, PORT)

filename = os.path.join("..", "sequences", Gene)
s = Seq()
s.read_fasta(filename)
print(f"Gene {Gene},  {s}")
gene_sequence = str(s)

for g in range(NUMBER_OF_FRAGMENTS + 1):
    start_index = g * 10
    end_index = start_index + 10
    fragment = gene_sequence[start_index: end_index]
    print(f"Fragment {g + 1}: {fragment} ")
