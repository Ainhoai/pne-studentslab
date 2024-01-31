c_a = 0
c_c = 0
c_g = 0
c_t = 0
dna_sequence = input("Please, enter a dna sequence: ")
for c in dna_sequence:
    if c == "A":
        c_a += 1
    elif c == "C":
        c_c += 1
    elif c == "G":
        c_g += 1
    elif c == "T":
        c_t += 1

total_count = c_a + c_c + c_g + c_t
print(total_count)
print("A:", c_a)
print("C:", c_c)
print("G:", c_g)
print("T:", c_t)

letters = {1: "A", 2: "C", 3: "G", 4: "T"}