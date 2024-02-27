from Seq1 import Seq
import os
PRACTICE = 1
EXERCISE = 10
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

Genes = ["ADA.txt", "FXN.txt", "U5.txt", "FRAT1.txt"]
for g in Genes:
    filename = os.path.join("..", "sequences", g)
    s = Seq()
    s.read_fasta(filename)
    print(f"Gene {g}: Most frequent bases: {s.max_base()}")

