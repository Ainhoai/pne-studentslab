class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.scores = []


    def __str__(self):  #el icono significa que estas heredando de la clase madre de la que viene el objeto. Tiene sentido crear herencias cuando tienes cosas en comun(caracteristicas o acciones).
        return f'Name{self.name}\nAge: {self.age}\nScores: {self.scores}'


    def is_older(self):
        """(f1) mejor hacerlo de otra forma:
        if self.age >= 18:
            return True
        else:
            return False """
        #(f2) mejor asi:
        return self.age >= 18

    def add_score(self, score):
        self.scores.append(score)


p1 = Person("Elena", 18)
print(f"Is she older? {p1.is_older()}")
p1.add_score(7.5)
print(p1) #no sirve si no está el método __str__


