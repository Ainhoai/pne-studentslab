import os
from Seq0 import *
genes = ["ADA", "FXN", "U5", "FRAT1"]
bases = ["A","G", "C", "T"]
for g in genes:
    filename = os.path.join("..", "sequence",  g + ".txt")
    dna_sequence = seq_read_fasta(filename)
    print(dna_sequence)
    for base in bases:
        print(base)