from pathlib import Path
import random
class Numberguesser:

    ATTEMPTS = 0
    secret_number = random.randint(1, 100)

    def __init__(self, secret_number, attempts):
        self.secret_number = secret_number
        self.attempts = attempts

    def guesser(self):
        if 0 <= self.player_number <= 100:
            Numberguesser.ATTEMPTS += 1
            print(f"You won after {Numberguesser.ATTEMPTS} attempts")
        elif self.player_number > 100:
            Numberguesser.ATTEMPTS += 1
            print(f"Lower")
        elif self.player_number < 100:
            Numberguesser.ATTEMPTS += 1
            print(f"Higher")
