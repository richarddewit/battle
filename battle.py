#!/usr/bin/env python3
import math
from os import RWF_HIPRI
from random import choice, randint
from threading import active_count


class Pokemon(object):
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


class Move(object):
    def __init__(self, name, hp_range):
        self._name = name
        self._hp_range = hp_range

    @property
    def name(self):
        return self._name

    def execute(self, target=None):
        raise NotImplementedError

    def calculate_hp(self):
        (min_hp, max_hp) = self._hp_range
        return randint(min_hp, max_hp)

    def learn_to(self, actor):
        self._actor = actor


class AttackingMove(Move):
    def execute(self, target):
        damage = self.calculate_hp()

        print("{actor}'s {move} does {damage} damage to {target}".format(
            actor=self._actor.name,
            move=self.name,
            damage=damage,
            target=target.name,
        ))
        target.update_hp(damage)


class HealingMove(Move):
    def execute(self):
        amount = self.calculate_hp()

        print("{actor}'s {move} heals {amount} hitpoints".format(
            actor=self._actor.name,
            move=self.name,
            amount=amount,
        ))
        self._actor.update_hp(amount * -1)


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


def main():
    player = Pokemon('Player', 100, [
        AttackingMove('Punch', (18, 25)),
        AttackingMove('Kick', (10, 35)),
        HealingMove('Eat Candybar', (18, 25)),
    ])
    computer = Pokemon('Computer', 100, [
        AttackingMove('Bleep', (18, 25)),
        AttackingMove('Throw Error', (10, 35)),
        HealingMove('Defragment', (18, 25)),
    ])
    game = Game(player, computer)

    actor = player
    target = computer
    turns = 0

    print('+' + ('-' * 58) + '+')

    while not game.ended:
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
            picked_move = actor.moves[random_index]
        else:
            if actor == computer:
                if actor.percent_hp > 90:
                    random_index = choice([0, 1])
                elif actor.percent_hp < 35:
                    random_index = choice([0, 1, 2])
                else:
                    random_index = choice([0] * 2 + [1] * 2 + [2] * 6)
                picked_move = actor.moves[random_index]
            else:
                print("It's your turn, pick a move!")
                picked_move = None
                while picked_move == None:
                    for ix, move in enumerate(actor.moves):
                        print("{index}: {move}".format(
                            index=ix + 1,
                            move=move.name))
                    i = input("Enter number: ")
                    try:
                        picked_move = actor.moves[int(i) - 1]
                    except:
                        print("Invalid choice")
                        print()

        if picked_move.__class__ == HealingMove:
            picked_move.execute()
        else:
            picked_move.execute(target)

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
