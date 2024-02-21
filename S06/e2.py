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


    def seq_list(self, seq_list):
        seq_list = [Seq("ACT"), Seq("GATA"), Seq("CAGATA")]

