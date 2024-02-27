from Seq1 import Seq

PRACTICE = 1
EXERCISE = 9
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")



s = Seq()

filename = ["U5.txt"]
dna_sequence = read_fasta("..", "sequences", filename)
s.read_fasta(filename)

