import os
from Seq0 import *
num = 20
dna_file = input("DNA file: ")
body = seq_read_fasta(os.path.join("..", "sequence", dna_file))
print("The first 20 bases are:", body[:num])
