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
        return len(self.strbases)


class Gene(Seq):
    """This class is derived from the Seq Class
           All the objects of class Gene will inherit
           the methods from the Seq class
        """
    def __init__(self, strbases, name= ""):
        super().__init__(strbases)
        self.name = name
        print("New Gene created")


    def __str__(self):
        return self.name + "-" + self.strbases
