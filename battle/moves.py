from random import randint


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


class DamagingMove(Move):
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
