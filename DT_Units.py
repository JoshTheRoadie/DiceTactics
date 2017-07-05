## Dice Tactics Units Module
## Will include Troop classes and Building Classes

import DiceRoller, DT_Board, pygame
from pygame.locals import *

class Troop:

    def __init__(self, owner, sides, move = 1, loc = (0, 0)):
        self.owner = owner
        self.sides = sides
        self.move = move
        self.loc = loc
        self.kills = 0

    def checkValidMoves(self, board):
        pass

    def attack(self, defender):
        '''Rolls the appropriate die for the attacker and defender.
        Returns the value of the attack roll, the defense roll, and True
        if the attacker won or False if the attacker lost in the form of
        a tuple:  (attack roll, defend roll, outcome)'''
        attack_roll = DiceRoller.roll(self.sides)
        defend_roll = DiceRoller.roll(defender.sides)
        if attack_roll > defend_roll:
            return (attack_roll, defend_roll, True)
        else:
            return (attack_roll, defend_roll, False)
    
    def __str__(self):
        return ('Owner: ' + self.owner + '\nSides: ' + str(self.sides)
                + '\nMove: ' + str(self.move) + '\nLoc: ' + str(self.loc)
                + '\nKills: ' + str(self.kills))
    
class Building:

    def __init__(self, owner, bldg = 'base', armor = 10, loc = (0, 0)):
        self.owner = owner
        self.bldg = bldg
        self.armor = armor
        self.loc = loc

    def __str__(self):
        return ('Owner: ' + self.owner + '\nBuilding: ' + self.bldg
                + '\nArmor: ' + str(self.armor) + '\nLoc: ' + str(self.loc))

# Action Functions for Troops

def checkValidMoves(troop, board):
    pass

if __name__ == '__main__':

    attacker = Troop('Player1', 20)
    defender = Troop('Player2', 12)
    loopcount = 1000
    loopdaloop = 50
    result_list = []
    for loops in range(loopdaloop):
        counter = 0
        for time in range(loopcount):
            result = attacker.attack(defender)
            if result[2] == True:
                counter += 1
        result_list.append(counter)
        print "Counter: " + str(counter) + "\nFalse: " + str(loopcount - counter)
    atk_win_percent = ((sum(result_list)/len(result_list))/float(loopcount)) * 100
    def_win_percent = 100 - atk_win_percent
    print ('Attacker with %d sides: ' % attacker.sides) + str(atk_win_percent) + '%'
    print ('Defender with %d sides: ' % defender.sides) + str(def_win_percent) + '%'
