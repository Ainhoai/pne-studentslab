import os
from Seq0 import *
N = 20
dna_file = input("DNA file: ")
dna_sequence = seq_read_fasta(os.path.join("..", "sequences", dna_file))
print(f"The first {N} bases are:")
print(dna_sequence[:N])
