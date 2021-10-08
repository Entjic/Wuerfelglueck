import collections

from model.dice import Dice
from model.team import Team


def turn(dice):
    score = dice.roll_dice()
    # print(score)
    return int(score) == 6


def simulate(pair):
    dice0 = pair.__getitem__(0)
    dice1 = pair.__getitem__(1)
    # print(str(dice0.identifier) + " vs " + str(dice1.identifier))
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
        if has_won(team0):
            # or not_possible_to_win_anymore(team1, dice1)
            return dice0.identifier
        team0.turn(team1)
        if has_won(team1):
            # or not_possible_to_win_anymore(team0, dice0):
            return dice1.identifier
        team1.turn(team0)


def has_won(team):
    counter = 0
    for stone in team.stones:
        if stone.position >= 40:
            counter += 1
    return counter == 4


def not_possible_to_win_anymore(team, dice):
    # todo check if team cannot win due to too high nr on their dice while being close to their home
    # fixme this shit does not work at all :(
    for stone in team.stones:
        if not can_be_brought_home(stone, dice, find_farthest_taken_position(team)):
            return True
    return False


def find_farthest_taken_position(team):
    value = 44
    if team.spot_blocked(43):
        value -= 1
        if team.spot_blocked(42):
            value -= 1
            if team.spot_blocked(41):
                value -= 1
    return value


def can_be_brought_home(stone, dice, farthest_taken_position):
    if stone.position >= farthest_taken_position:
        return True

    for side in dice.sides:
        if int(side) + int(stone.position) < farthest_taken_position:
            return True
    return False


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


if __name__ == '__main__':
    print("simulation started")
    dices_read = read_dices_from_file(2)

    amount_of_simulations = 1000
    pairs_to_play = create_all_possible_combinations(dices_read)

    amount_of_wins = []

    for i in range(amount_of_simulations):
        for pair in pairs_to_play:
            # print(f'Pair {counter} dice {pair.__getitem__(0).identifier}: ' + pair.__getitem__(0).info())
            # print(f'Pair {counter} dice {pair.__getitem__(1).identifier}: ' + pair.__getitem__(1).info())
            winning = simulate(pair)
            # print(winning)
            # print(collections.Counter(rolled).values())
            rolled = []
            # print(winning)
            amount_of_wins.append(winning)
            # print(collections.Counter(amount_of_wins))

    print("Final : " + str(collections.Counter(amount_of_wins)))
    # for pair in pairs_to_play:
    #     print(f'Dice 0: {pair.__getitem__(0).identifier}')
    #     print(f'Dice 1: {pair.__getitem__(1).identifier}')
    #     print('---')
    print(f'Played Games: {amount_of_simulations * len(pairs_to_play)}')
    # simulate_dice(dices_read[2])
