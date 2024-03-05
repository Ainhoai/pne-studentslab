from Seq1 import Seq
from client0 import Client
import os
genes = ["ADA.txt", "FXN.txt", "U5.txt", "FRAT1.txt"]

for gene in genes:
    filename = os.path.join("..", "sequences",  gene)

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
