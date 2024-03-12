from pathlib import Path


class Seq:
    """ A class to represent  sequences """
    BASES = ["A", "G", "C", "T"]

    def __init__(self, strbases= None):
        if strbases is None or len(strbases) == 0:
            self.strbases = "NULL"
            print("NULL sequence created.")
        else:
            ok = True
            for b in strbases:
                if b not in Seq.BASES:
                    ok = False
                    self.strbases = "ERROR!"
                    print("Incorrect sequence detected.")
                    break
            if ok:
                self.strbases = strbases
                print("A new sequence is created!")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR!":
            return 0
        return len(self.strbases)

    def count_bases(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR!":
            return 0
        return self.strbases.count(base)

    def count(self):
        base_appearances = {}
        for base in Seq.BASES:
            base_appearances[base] = self.count_bases(base)
        return base_appearances

    def reverse(self):
        if self.strbases == "NULL":
            return "NULL"

        elif self.strbases == "ERROR!":
            return "ERROR!"
        else:
            new_seq = self.strbases[:]
            return new_seq[::-1]

    def complement(self):
        if self.strbases == "NULL":
            return "NULL"

        elif self.strbases == "ERROR!":
            return "ERROR!"
        else:
            bases_complement = {"A": "T", "T": "A", "C": "G", "G": "C"}
            comp = ""
            for base in self.strbases:
                comp += bases_complement[base]
            return comp

    def read_fasta(self, filename):
        file_content = Path(filename).read_text()
        lines = file_content.splitlines()
        body = lines[1:]

        dna_sequence = ""
        for line in body:
            dna_sequence += line
        self.strbases = dna_sequence

    def max_base(self):
        bases_dict = {}
        for b in Seq.BASES:
            bases_dict[b] = self.count_bases(b)
        most_frequent_base = max(bases_dict, key=bases_dict.get)

        return most_frequent_base

    def info(self):
        s = f"Sequence: {self.strbases}\n"
        s += f"Total length: {self.len()}\n"
        for base, count in self.count().items(): #me devuelve en cada vuelta una pareja ("A: 3"; p.ej)
            if self.strbases == "NULL" or self.strbases == "ERROR!":
                percentage = 0
            else:
                percentage = (count * 100) / self.len()
                #percentage = round(percentage, 2)
            s += f"{base}: {count} ({percentage:.1f}) %\n"
        return s





class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New Gene created")



    def __str__(self):
        return self.name + "-" + self.strbases
