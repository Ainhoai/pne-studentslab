class car:
    def __init__(self, brand, speed= 0):
        self.car_brand = brand
        self.speed = speed
    def set_speed(self, speed):
        self.speed = speed
class Ferrari(car):
    pass

mycar = car("Renault")
yourcar = Ferrari("Ferrari")
print(yourcar.car_brand)