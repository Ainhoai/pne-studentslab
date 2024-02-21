import os
from Seq0 import *


def most_frequent_base(dna_sequence):
    max_base = ""
    max_count = 0
    for base in BASES:
        count = seq_count_base(dna_sequence, base)
        if count > max_count:
            max_count = count
            max_base = base
    return max_base


GENES = ["U5", "ADA", "FRAT1", "FXN"]
BASES = ["A", "C", "T", "G"]

for gene in GENES:
    filename = os.path.join("..", "sequences", gene + ".txt")
    dna_sequence = seq_read_fasta(filename)
    print(f"Gene {gene}: {most_frequent_base(dna_sequence)}")
