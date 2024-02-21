import os
from Seq0 import *

genes = "U5"
N = 20

filename = os.path.join("..", "sequences", genes + ".txt")
dna_sequence = seq_read_fasta(filename)
fragment = dna_sequence[:N]
print(f"Gene {genes}")
print(f"Fragment: {fragment}")
print(f"Reverse: {seq_reverse(dna_sequence, N)}")
