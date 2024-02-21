import os
from Seq0 import *

genes = ["U5", "ADA", "FRAT1", "FXN"]

for gene in genes:
    filename = os.path.join("..", "sequences", gene + ".txt")
    dna_sequence = seq_read_fasta(filename)
    print(f"Gene {gene}: {seq_count(dna_sequence)}")
