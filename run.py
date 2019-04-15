#!/usr/bin/env python3
import argparse

from battle.character import Character
from battle.moves import DamagingMove, HealingMove
from battle.game import Game


def main():
    parser = argparse.ArgumentParser(description='Turn-based battle game')
    parser.add_argument('--auto', action='store_true',
                        help='Automatically chose moves')
    args = parser.parse_args()

    player = Character('Player', 100, [
        DamagingMove('Punch', (18, 25)),
        DamagingMove('Kick', (10, 35)),
        HealingMove('Eat Candybar', (18, 25)),
    ])
    computer = Character('Computer', 100, [
        DamagingMove('Bleep', (18, 25)),
        DamagingMove('Throw Error', (10, 35)),
        HealingMove('Defragment', (18, 25)),
    ])
    game = Game(player, computer)

    print('+' + ('-' * 58) + '+')

    while not game.ended:
        game.print_game_status()

        if args.auto or game.is_computers_turn:
            game.pick_random_move()
        else:
            print("It's your turn, pick a move!")
            game.pick_move()

        game.do_picked_move()

        game.swap_turn()
        print('+' + ('-' * 58) + '+')

    game.announce_winner()


if __name__ == "__main__":
    main()
