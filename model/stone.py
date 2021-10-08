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
