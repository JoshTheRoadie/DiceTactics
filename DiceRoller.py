## DICE ROLLER MODULE  By: Joshua McCready
## A group of functions to roll dice of any type and return the sum or the
## individual dice.

import random

def roll(sides=6):
    '''Rolls a single die and returns the result.'''
    return random.randint(1, sides)

def roll_dice(num_dice=1, sides=6):
    '''Returns a list containing the values of each die rolled.  num_dice is
    the number of dice rolled.  sides is the type of dice rolled.'''

    dice = []
    i = 0
    while i < num_dice:
        dice.append(random.randint(1, sides))
        i += 1
    return dice


def roll_sum(num_dice=1, sides=6):
    '''Returns the sum of a dice roll.  num_dice is the number of dice rolled.
    sides is the type of dice rolled.  Both arguments should be given as
    integers. '''

    total = 0
    i = 0
    while i < num_dice:
        total = total + random.randint(1, sides)
        i += 1
    return total


if __name__ == '__main__':
    print 'DiceRoller.py\nA module for rolling dice of any variety.'
    
