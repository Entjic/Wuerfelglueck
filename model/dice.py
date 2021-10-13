import random


class Dice:
    def __init__(self, amount_of_sides, sides, identifier):
        self.amount_of_sides = amount_of_sides
        self.sides = []
        for side in sides:
            self.sides.append(int(side))
        self.identifier = identifier

    def roll_dice(self):
        # print(self.sides)
        choice = random.choice(self.sides)
        # print(str(self.sides) + " -> " + str(choice))
        return choice

    def info(self):
        return f'Dice got {self.amount_of_sides} sides: {self.sides}'
