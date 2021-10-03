import collections
import random

rolled = []


class Team:
    def __init__(self, identifier, dice):
        self.identifier = identifier
        self.dice = dice
        self.stones = Stone(identifier, 0), Stone(identifier, 1), Stone(identifier, 2), Stone(identifier, 3)

    def spawn(self):
        for stone in self.stones:
            if stone.position == -1:
                stone.spawn()

    def roll_dice(self):
        return self.dice.roll_dice()

    def turn(self, enemy):
        score = int(self.roll_dice())
        rolled.append(score)
        print(score)
        if score == 6:
            print('rolled 6')
            if self.can_spawn_new_stone():
                print("use 6 to spawn")
                self.spawn_new_stone()
                self.print_debug()
            else:
                print("use 6 as move")
                self.handle_move(score, enemy)
                self.print_debug()
            print("roll again")
            return self.turn(enemy)
        print("handle move")
        self.handle_move(score, enemy)
        self.print_debug()

    def handle_move(self, score, enemy):
        stone = self.get_farthest_away_movable_stone(score)
        if self.is_spawn_blocked():
            stone = self.get_closest_movable_stone(score)
        if stone is None:
            print("No valid stone could be found")
            return
        stone.move(score)
        if enemy.conflicts_other_team_stone(stone):
            print("kick enemy stone on position " + str(stone.position))
            enemy.get_conflicted_stone_other_team(stone).position = -1

    def get_farthest_away_movable_stone(self, score):
        farthest = None
        for stone in self.stones:
            if not self.can_move(stone, score):
                continue
            if farthest is None or farthest.position < stone.position:
                farthest = stone
        return farthest

    def can_spawn_new_stone(self):
        if self.spot_blocked(0):
            return False
        spawnable_stones = 0
        for stone in self.stones:
            if stone.position == -1:
                spawnable_stones += 1
        return spawnable_stones != 0

    def is_spawn_blocked(self):
        return self.spot_blocked(0)

    def get_stone_to_unblock_spawn(self, score):
        return self.get_closest_movable_stone(score)

    def get_closest_movable_stone(self, score):
        closest = None
        for stone in self.stones:
            if not self.can_move(stone, score):
                continue
            if closest is None or closest.position > stone.position:
                closest = stone
        return closest

    def spot_blocked(self, spot):
        for stone in self.stones:
            if stone.position == spot:
                return True
        return False

    def get_stone_on_spot(self, spot):
        for stone in self.stones:
            if stone.position == spot:
                return stone
        return None

    def spawn_new_stone(self):
        for stone in self.stones:
            if stone.position == -1:
                stone.spawn()
                return

    def conflicts_other_team_stone(self, stone):
        # todo protect home!
        for s in self.stones:

            if s.position >= 40:
                continue

            if int(s.position) == int(stone.position):
                continue

            relative_position_self = int(s.position) % 20
            relative_position_enemy = int(stone.position) % 20

            if relative_position_self == relative_position_enemy:
                return True
        return False

    def get_conflicted_stone_other_team(self, stone):
        for s in self.stones:
            relative_position_self = int(s.position)
            if relative_position_self + 20 >= 40:
                relative_position_self = relative_position_self + 20
            relative_position_enemy = int(stone.position)
            if relative_position_enemy + 20 >= 40:
                relative_position_enemy = relative_position_enemy + 20

            if relative_position_self == relative_position_enemy:
                return s
        return None

    def can_move(self, stone, score):
        if stone.position == -1 or stone.position + score > 43:
            return False
        # print(stone.info() + " is on board")
        return not self.will_conflicts_other_stone(stone, score)

    def will_conflicts_other_stone(self, stone, score):
        for s in self.stones:
            if s.position == stone.position + score:
                return True
        return False

    def print_debug(self):
        debug = "Debug: "
        for stone in self.stones:
            debug += stone.info()
            debug += ' '
        print(debug)


class Stone:
    def __init__(self, team, identifier):
        self.team = team
        self.identifier = identifier
        self.position = -1

    def spawn(self):
        self.position = 0

    def move(self, amount):
        self.position += amount

    def info(self):
        return f'[{self.team} nr {self.identifier} pos: {self.position}]'


class Dice:
    def __init__(self, amount_of_sides, sides, identifier):
        self.amount_of_sides = amount_of_sides
        self.sides = sides
        self.identifier = identifier

    def roll_dice(self):
        # print(self.sides)
        choice = random.choice(self.sides)
        # print(str(self.sides) + " -> " + str(choice))
        return choice

    def info(self):
        return f'Dice got {self.amount_of_sides} sides: {self.sides}'


def turn(dice):
    score = dice.roll_dice()
    # print(score)
    return int(score) == 6


def simulate(pair):
    dice0 = pair.__getitem__(0)
    dice1 = pair.__getitem__(1)
    print(str(dice0.identifier) + " vs " + str(dice1.identifier))
    if impossible_to_win(dice0) is True:
        return dice1.identifier

    if (impossible_to_win(dice1)) is True:
        return dice0.identifier

    return simulate_game(pair)


def simulate_game(pair):
    dice0 = pair.__getitem__(0)
    dice1 = pair.__getitem__(1)
    team0 = Team(0, dice0)
    team1 = Team(1, dice1)
    while True:
        team0.turn(team1)
        if has_won(team0) is True:
            return dice1.identifier
        team1.turn(team0)
        if has_won(team1) is True:
            return dice0.identifier


def has_won(team):
    counter = 0
    for stone in team.stones:
        if stone.position >= 40:
            counter += 1
    return counter == 4


def impossible_to_win(dice):
    for side in dice.sides:
        if int(side) == 6:
            return False
    return True


def read_dices_from_file(nr):
    dices = []
    with open(f'resources/wuerfel{nr}.txt') as file:
        lines = file.readlines()

    amount_of_dices = lines.__getitem__(0)
    for x in range(0, int(amount_of_dices)):
        dice = lines.__getitem__(x + 1).rstrip('\n').split(' ')
        amount_of_sides = int(dice.__getitem__(0))
        sliced_array = dice[1:amount_of_sides + 1]
        dices.append(Dice(amount_of_sides, sliced_array, x))
    return dices


def create_all_possible_combinations(dices):
    tuples = []
    for x in dices:
        for y in dices:
            if x == y:
                continue
            tuples.append((x, y))
    return tuples


def simulate_dice(dice):
    nr = []
    for _ in range(100000):
        nr.append(int(dice.roll_dice()))
    print(collections.Counter(nr).values())


if __name__ == '__main__':
    print("simulation started")
    dices_read = read_dices_from_file(2)

    counter = 0

    amount_of_wins = []
    for i in range(10):
        for pair in create_all_possible_combinations(dices_read):
            print(f'Pair {counter} dice {pair.__getitem__(0).identifier}: ' + pair.__getitem__(0).info())
            print(f'Pair {counter} dice {pair.__getitem__(1).identifier}: ' + pair.__getitem__(1).info())
            winning = simulate(pair)
            print(winning)
            # print(collections.Counter(rolled).values())
            rolled = []
            # print(winning)
            amount_of_wins.append(winning)
            print(collections.Counter(amount_of_wins))
            counter += 1

    print("games played " + str(counter))
    print("Final : " + str(collections.Counter(amount_of_wins)))

    # simulate_dice(dices_read[2])
