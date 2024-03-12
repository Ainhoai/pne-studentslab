import os
from Seq0 import *

GENE = "U5"
N = 20

filename = os.path.join("..", "sequences", GENE + ".txt")

dna_sequence = seq_read_fasta(filename)
fragment = dna_sequence[:N]
print(f"Gene {GENE}")
print(f"Fragment: {fragment}")
print(f"Complement: {seq_complement(fragment)}")
