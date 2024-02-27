from Seq1 import Seq
import os
PRACTICE = 1
EXERCISE = 9
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")


s = Seq()
Gene = "U5.txt"
filename = os.path.join("..", "sequences", Gene)
s.read_fasta(filename)
print(f"Sequence: (Length: {s.len()}) {s}\nBases: {s.count()}\nRev: {s.reverse()}\nComp: {s.complement()}")

