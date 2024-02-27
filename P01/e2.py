from Seq1 import Seq

PRACTICE = 1
EXERCISE = 2
print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")
seq_list = [Seq(), Seq("TATAC")]
for i, s in enumerate(seq_list):
    print(f"Sequence {i + 1}: {s}")

