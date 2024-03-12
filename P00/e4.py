import os
from Seq0 import *
genes = ["ADA.txt", "FXN.txt", "U5.txt", "FRAT1.txt"]
bases = ["A", "G", "C", "T"]
for gene in genes:
    filename = os.path.join("..", "sequences",  gene)
    dna_sequence = seq_read_fasta(filename)
    print(f"Gene {gene}:")
    for base in bases:
        print(f"{base}: {seq_count_base(dna_sequence, base)}")
