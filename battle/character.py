class Character(object):
    def __init__(self, name, hitpoints=100, moves=[]):
        self._name = name
        self._hitpoints = hitpoints
        self._max_hp = hitpoints
        self._moves = []

        for move in moves:
            move.learn_to(self)
            self._moves.append(move)

    @property
    def name(self):
        return self._name

    @property
    def hitpoints(self):
        return self._hitpoints

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def percent_hp(self):
        return int(self._hitpoints / self._max_hp * 100)

    @property
    def moves(self):
        return self._moves

    def update_hp(self, amount):
        new_value = self._hitpoints - amount
        self._hitpoints = min(100, max(0, new_value))
