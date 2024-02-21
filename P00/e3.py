import os
from Seq0 import *

genes = ["ADA.txt", "FXN.txt", "U5.txt", "FRAT1.txt"]
for gene in genes:
    filename = os.path.join("..", "sequences", gene)
    dna_sequence = seq_read_fasta(filename)
    print(f"Gene {gene} -> Length: {seq_len(dna_sequence)}")
