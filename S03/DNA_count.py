
dna_sequence = input("Please, enter a dna sequence: ")
letters = {"A":  0, "C": 0, "G": 0, "T": 0}
for c in dna_sequence:
    if c == "A":
        letters["A"] += 1
    elif c == "C":
        letters["C"] += 1
    elif c == "G":
        letters["G"] += 1
    elif c == "T":
        letters["T"] += 1

total_count = len(dna_sequence)
print(total_count)
for x, y in letters.items():
    print("{}: {}".format(x, y))
