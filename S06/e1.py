class Seq:
    """ A class to represent  sequences """

    def __init__(self, strbases):
        bases = ["A", "G", "C", "T"]
        for b in strbases:
            if b not in bases:
                self.strbases = "ERROR!"
                print("Incorrect sequence detected.")
                return

        self.strbases = strbases
        print("A new sequence is created!")
    def __str__(self):
        return self.strbases


s1 = Seq("ACCTGC")
s2 = Seq("Hello? Am I a valid sequence?")
print(f"Sequence 1: {s1}")
print(f"Sequence 2: {s2}")