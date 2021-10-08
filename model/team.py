from model.stone import Stone


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
        # print(score)
        if score == 6:
            # print('rolled 6')
            if self.can_spawn_new_stone():
                # print("use 6 to spawn")
                self.spawn_new_stone()
                # self.print_debug()
            else:
                # print("use 6 as move")
                self.handle_move(score, enemy)
                # self.print_debug()
            # print("roll again")
            return self.turn(enemy)
        # print("handle move")
        self.handle_move(score, enemy)
        # self.print_debug()

    def handle_move(self, score, enemy):
        stone = self.get_farthest_away_movable_stone(score)
        if self.is_spawn_blocked():
            stone = self.get_closest_movable_stone(score)
        if stone is None:
            # print("No valid stone could be found")
            return
        stone.move(score)
        if enemy.conflicts_other_team_stone(stone):
            # print("kick enemy stone on position " + str(stone.position))
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
        for s in self.stones:

            if s.position >= 40:
                continue

            if s.position < 0:
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

            if s.position >= 40:
                continue

            if s.position < 0:
                continue

            if int(s.position) == int(stone.position):
                continue

            relative_position_self = int(s.position) % 20
            relative_position_enemy = int(stone.position) % 20

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
