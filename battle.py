#!/usr/bin/env python3
import math
from random import choice, randint


class Pokemon(object):
    def __init__(self, name, hitpoints=100, moves=[]):
        self._name = name
        self._hitpoints = hitpoints
        self._max_hp = hitpoints
        # self._moves = []

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

    # @property
    # def moves(self):
    #     return self._moves

    # def add_move(self, name, damage_range):
    #     self._moves.append(Move(name, damage_range))

    def take_damage(self, amount):
        self._hitpoints -= amount
        if self._hitpoints < 0:
            self._hitpoints = 0
        elif self._hitpoints > 100:
            self._hitpoints = 100


class Move(object):
    def __init__(self, name, damage_range, heal=False):
        self._name = name
        self._damage_range = damage_range
        self._is_heal = heal

    @property
    def name(self):
        return self._name

    @property
    def is_heal(self):
        return self._is_heal

    def execute(self, actor, target=None):
        damage = self.calculate_damage()
        if self._is_heal:
            self.heal(damage, actor)
        else:
            self.deal_damage(damage, actor, target)

    def deal_damage(self, damage, actor, target):
        print("{actor}'s {move} does {damage} damage to {target}".format(
            actor=actor.name,
            move=self.name,
            damage=damage,
            target=target.name,
        ))
        target.take_damage(damage)

    def heal(self, amount, actor):
        print("{actor}'s {move} heals {amount} damage".format(
            actor=actor.name,
            move=self.name,
            amount=amount,
        ))
        actor.take_damage(amount * -1)

    def calculate_damage(self):
        (min_damage, max_damage) = self._damage_range
        return randint(min_damage, max_damage)


# class Game(object):
#     _player = None
#     _computer = None
#     _moves = []
#     _actor = None
#     _target = None

#     def set_player(self, name, hitpoints=100):
#         self._player = Pokemon(name, hitpoints)

#     def set_computer(self, name, hitpoints=100):
#         self._computer = Pokemon(name, hitpoints)


def main():
    player = Pokemon('Feraligatr', 100)
    computer = Pokemon('Exeggutor', 100)
    moves = [
        Move('Tackle', (18, 25)),
        Move('Body Slam', (10, 35)),
        Move('Heal', (18, 25), heal=True),
    ]

    actor = player
    target = computer
    turns = 0

    print('+' + ('-' * 58) + '+')

    while player.hitpoints > 0 and computer.hitpoints > 0:
        print(
            "{left}{right}".format(
                left="| {name}: {hitpoints}HP |".format(
                    name=player.name,
                    hitpoints=str(player.hitpoints).rjust(3),
                ).ljust(30),
                right="| {name}: {hitpoints}HP |".format(
                    name=computer.name,
                    hitpoints=str(computer.hitpoints).rjust(3),
                ).rjust(30),
            ))
        print('|' + (' ' * 58) + '|')

        auto = True
        if auto:
            if actor.percent_hp > 90:
                random_index = choice([0, 1])
            elif actor.percent_hp < 35:
                random_index = choice([0, 1, 2])
            else:
                random_index = choice([0] * 2 + [1] * 2 + [2] * 6)
            picked_move = moves[random_index]
        else:
            if actor == computer:
                if actor.percent_hp > 90:
                    random_index = choice([0, 1])
                elif actor.percent_hp < 35:
                    random_index = choice([0, 1, 2])
                else:
                    random_index = choice([0] * 2 + [1] * 2 + [2] * 6)
                picked_move = moves[random_index]
            else:
                print("It's your turn, pick a move!")
                picked_move = None
                while picked_move == None:
                    for ix, move in enumerate(moves):
                        print("{index}: {move}".format(
                            index=ix + 1,
                            move=move.name))
                    i = input("Enter number: ")
                    try:
                        picked_move = moves[int(i) - 1]
                    except:
                        print("Invalid choice")
                        print()

        picked_move.execute(actor, target)

        # Swap turns
        actor, target = target, actor
        turns += 1
        print('+' + ('-' * 58) + '+')

    if player.hitpoints == 0:
        print("{name} wins with {hitpoints} hitpoints left after {turns} turns. Better luck next time!".format(
            name=computer.name,
            hitpoints=computer.hitpoints,
            turns=math.ceil(turns / 2),
        ))
        exit(0)

    if computer.hitpoints == 0:
        print("{name} wins with {hitpoints} hitpoints left after {turns} turns. Congratulations!".format(
            name=player.name,
            hitpoints=player.hitpoints,
            turns=math.ceil(turns / 2),
        ))
        exit(0)


if __name__ == "__main__":
    main()
