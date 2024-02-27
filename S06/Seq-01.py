class Seq:
    """ A class to represent  sequences """
    def __init__(self, strbases):
        self.strbases = strbases
        print("New sequences created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)


class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """
    def __init__(self, strbases, name= ""):
        super().__init__(strbases)
        self.name = name
        print("New Gene created!")



s1 = Seq("AGTACACTGGT")
s2 = Seq("CGTAAC")

print(f"Sequence 1: {s1}")
print(f"  Length: {s1.len()}")
print(f"Sequence 2: {s2}")
print(f"  Length: {s2.len()}")




