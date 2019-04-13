import math
from random import choice

from .moves import DamagingMove, HealingMove


class Game(object):
    _player = None
    _computer = None
    _actor = None
    _target = None
    _turns = 0
    _picked_move = None

    def __init__(self, player, computer):
        self._player = player
        self._computer = computer
        self._actor = self._player
        self._target = self._computer

    @property
    def turns(self):
        return self._turns

    @property
    def ended(self):
        return self._player.hitpoints == 0 or self._computer.hitpoints == 0

    @property
    def is_players_turn(self):
        return self._actor == self._player

    @property
    def is_computers_turn(self):
        return self._actor == self._computer

    def swap_turn(self):
        self._actor, self._target = self._target, self._actor
        self._turns += 1
        self._picked_move = None

    def pick_random_move(self):
        if self._actor.percent_hp > 90:
            random_index = choice([0, 1])
        elif self._actor.percent_hp < 35:
            random_index = choice([0, 1, 2])
        else:
            random_index = choice([0] * 2 + [1] * 2 + [2] * 6)
        self._picked_move = self._actor.moves[random_index]

    def pick_move(self):
        picked_move = None
        while picked_move == None:
            for ix, move in enumerate(self._actor.moves):
                print("{index}: {move}".format(
                    index=ix + 1,
                    move=move.name))
            i = input("Enter number: ")
            try:
                picked_move = self._actor.moves[int(i) - 1]
            except:
                print("Invalid choice")
                print()
        self._picked_move = picked_move

    def do_picked_move(self):
        if self._picked_move.__class__ == HealingMove:
            self._picked_move.execute()
        else:
            self._picked_move.execute(self._target)

    def announce_winner(self):
        if self._player.hitpoints == 0:
            print("{name} wins with {hitpoints} hitpoints left after {turns} turns. Better luck next time!".format(
                name=self._computer.name,
                hitpoints=self._computer.hitpoints,
                turns=math.ceil(self._turns / 2),
            ))

        elif self._computer.hitpoints == 0:
            print("{name} wins with {hitpoints} hitpoints left after {turns} turns. Congratulations!".format(
                name=self._player.name,
                hitpoints=self._player.hitpoints,
                turns=math.ceil(self._turns / 2),
            ))

        else:
            print("The match hasn't ended yet!")

    def print_game_status(self):
        print(
            "{left}{right}".format(
                left="| {name}: {hitpoints}HP |".format(
                    name=self._player.name,
                    hitpoints=str(self._player.hitpoints).rjust(3),
                ).ljust(30),
                right="| {name}: {hitpoints}HP |".format(
                    name=self._computer.name,
                    hitpoints=str(self._computer.hitpoints).rjust(3),
                ).rjust(30),
            ))
        print('|' + (' ' * 58) + '|')
