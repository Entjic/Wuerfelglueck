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
        if has_won(team0) or not possible_to_bring_next_stone_home(team1):
            return dice0.identifier
        team0.turn(team1)
        if has_won(team1) or not possible_to_bring_next_stone_home(team0):
            return dice1.identifier
        team1.turn(team0)


def has_won(team):
    counter = 0
    for stone in team.stones:
        if stone.position >= 40:
            counter += 1
    return counter == 4


def possible_to_bring_next_stone_home(team):
    stones_that_are_not_already_home = get_stones_that_are_not_already_home_sorted_by_size_down(team)
    if len(stones_that_are_not_already_home) == 0:
        return True
    stone_to_check = stones_that_are_not_already_home.__getitem__(0)
    val = can_be_brought_home(stone_to_check, team.dice, get_spot_to_target(team))
    # if not val:
    #     print("ITS NOT POSSIBLE TO WIN THE GAME IN THIS POSITION ANY LONGER FOR TEAM " + str(team.identifier)
    #           + " WITH DICE " + team.dice.info())
    return val


def can_be_brought_home(stone, dice, target_home_position):
    for side in dice.sides:
        if side == 0:
            continue
        if side <= (target_home_position - stone.position):
            return True
    return False


def get_stones_that_are_not_already_home_sorted_by_size_down(team):
    sorted_stones = get_stones_sorted(team)

    last_taken_spot = 43
    stones_that_are_not_already_home = []

    for stone in sorted_stones:
        if stone.position == last_taken_spot:
            last_taken_spot -= 1
        else:
            stones_that_are_not_already_home.append(stone)

    return stones_that_are_not_already_home


def get_spot_to_target(team):
    sorted_stones = get_stones_sorted(team)

    spot_to_target = 43
    for stone in sorted_stones:
        if stone.position == spot_to_target:
            spot_to_target -= 1

    return spot_to_target


def get_stones_sorted(team):
    sorted_stones = []
    for stone in team.stones:
        sorted_stones.append(stone)
    sorted_stones.sort(key=lambda s: s.position, reverse=True)
    return sorted_stones


def get_smallest_side_of_dice(dice):
    smallest = 0
    for side in dice.sides:
        if side > smallest:
            smallest = side
    return smallest


def impossible_to_win(dice):
    for side in dice.sides:
        if side == 6:
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


def simulate_all_dices():
    print(f'simulation for file {str(file_number)} started')
    dices_read = read_dices_from_file(file_number)
    pairs_to_play = create_all_possible_combinations(dices_read)
    amount_of_wins = []
    for i in range(amount_of_simulations):
        for pair in pairs_to_play:
            # print(f'Pair {counter} dice {pair.__getitem__(0).identifier}: ' + pair.__getitem__(0).info())
            # print(f'Pair {counter} dice {pair.__getitem__(1).identifier}: ' + pair.__getitem__(1).info())
            winning = simulate(pair)
            # print("--GAME-OVER--")
            # print(f'winning dice was {str(winning)}')
            # print(winning)
            # print(collections.Counter(rolled).values())
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


if __name__ == '__main__':
    file_number = 5
    amount_of_simulations = 1000
    simulate_all_dices()
