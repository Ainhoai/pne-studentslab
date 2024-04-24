def are_bases_ok(strbases):
    ok = True
    for c in strbases:
        if c not in Seq.BASES:
            ok = False
            break
    return ok


class Seq:
    """A class for representing sequences"""
    BASES = ['A', 'T', 'C', 'G']
    COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    VALUES = {'A': 3, 'T': -1, 'C': 2, 'G': 7}

    def __init__(self, strbases=None):
        if strbases is None or len(strbases) == 0:
            self.strbases = "NULL"
            print("NULL sequence created")
        elif are_bases_ok(strbases):
            self.strbases = strbases
            print("New sequence created!")
        else:
            self.strbases = "ERROR"
            print("INCORRECT Sequence detected")

    def __str__(self):
        return self.strbases

    def len(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return len(self.strbases)

    def count_base(self, base):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        return self.strbases.count(base)

    def count(self):
        bases_appearances = {}
        for base in Seq.BASES:
            bases_appearances[base] = self.count_base(base)
        return bases_appearances

    def reverse(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        return self.strbases[::-1]

    def complement(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return self.strbases
        result = ""
        for base in self.strbases:
            result += Seq.COMPLEMENTS[base]
        return result

    def read_fasta(self, filename):
        from pathlib import Path

        file_content = Path(filename).read_text()
        lines = file_content.splitlines()
        self.strbases = ""
        for line in lines[1:]:
            self.strbases += line

    def most_frequent_base(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return None
        max_base = ""
        max_count = 0
        for base in Seq.BASES:
            count = self.count_base(base)
            if count > max_count:
                max_count = count
                max_base = base
        return max_base

    def info(self):
        s = f"Total length: {self.len()}\n"
        for base, count in self.count().items():
            if self.len() != 0:
                percentage = (count * 100) / self.len()
            else:
                percentage = 0
            s += f"{base}: {count} ({percentage:.1f} %)\n"
        return s

    def multiplication(self):
        if self.strbases == "NULL" or self.strbases == "ERROR":
            return 0
        result = 1
        for base in self.strbases:
            result *= Seq.VALUES[base]
        return result


class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """
    def __init__(self, strbases, name=""):
        super().__init__(strbases)
        self.name = name
        print("New gene created")

    def __str__(self):
        """Print the Gene name along with the sequence"""
        return self.name + "-" + self.strbases