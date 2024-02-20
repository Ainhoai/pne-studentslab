class vehicle:   #THE MOTHER CLASS :)
    def set_speed(self, speed):
        self.speed = speed

class car(vehicle):
    def __init__(self, brand, speed= 0):
        self.car_brand = brand
        self.speed = speed
    def set_speed(self, speed):
        self.speed = speed
class Ferrari(car):
    def __int__(self):
        super().__init__("Ferrari")  #with super we call the mother class since we have created a new init.
        self.music = "classic"

    def make_cabrio(self):
        self.speed = 20
        self.music = "loud"
        return "wow"

mycar = car("Renault")
yourcar = Ferrari("Ferrari", 100)   #----> __init__
print(yourcar.car_brand)
yourcar.set_speed(120)
print(yourcar.speed)

print(yourcar.make_cabrio(), "and music is", yourcar.music, "and speed is", yourcar.speed)