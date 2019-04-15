# Battle: A Turn Based Pokemon Style Game

## Up and Running

```shell
git clone git@github.com:richarddewit/battle.git
cd battle
./run.py

# Or for auto-combat (no input)
./run.py --auto
```

## TODO

- [x] Make "auto-combat" a cli-flag instead of a hardcoded boolean
- [ ] Separate messages into `Message` class
- [ ] Generalize random move selection, is now hardcoded into indexes (`[0, 1]` and `[0, 1, 2]` instead of checking which move is a `HealingMove`)

## The Project
### GOAL

Write a **simple game** that allows the **user** and the **computer** to take **turns** selecting **moves** to use against each other. Both the computer and the player should start out at the same amount of **health** (such as 100), and should be able to choose between the three moves:

1. The first move should do moderate **damage** and has a small **range** (such as 18-25).
2. The second move should have a large range of damage and can deal high or low damage (such as 10-35). 
3. The third move should **heal** whoever casts it a moderate amount, similar to the first move.

After each move, a **message** should be printed out that tells the user what just happened, and how much health the user and computer have. Once the user or the computer's health reaches 0, the game should end.

### SUBGOALS

1. When someone is defeated, make sure the game prints out that their health has reached 0, and not a negative number. 
2. When the computer's health reaches a set amount (such as 35%), increase it's chance to cast heal. 
3. Give each move a name.
