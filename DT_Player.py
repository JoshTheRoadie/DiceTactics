## Player module for Dice Tactics

import DT_Pieces, DiceRoller, pygame
from DT_Constants import *



class Player:
    
    def __init__(self, name, color, economy, money = 0):
        self.name = name
        self.color = color
        self.economy = economy
        self.money = money
        self.bldgs = []
        self.troops = []

    def addBuildingList(self, building_list):
        self.bldgs = building_list

    def addTroopList(self, troop_list):
        self.troops = troop_list

    def rollEconomyDice(self):
        dice = DiceRoller.roll_dice(self.economy)
        self.money = self.money + sum(dice)
        return dice
        
    def updatePiecesOnBoard(self, board):
        for building in self.bldgs:
            board.placeItem(building, building.loc)
        for troop in self.troops:
            board.placeItem(troop, troop.loc)

    def buyTroop(self, sprite_dict, sides):
        image1_key = self.color + ('d%d' % (sides,))
        image2_key = 'dark' + self.color + ('d%d' % (sides,))
        image_list = [sprite_dict[image1_key], sprite_dict[image2_key]]
        troop = DT_Pieces.Troop(image_list, (None,None), self.color,
                                sides)
        self.troops.append(troop)
        self.money = self.money - TROOPCOSTS[sides]
        return troop

    def findAllVisibleTiles(self, board):
        visible_tiles = []
        for troop in self.troops:
            visible_tiles = visible_tiles + troop.findVisibleTiles(board)
        return list(set(visible_tiles))
    
    #PYGAME DRAWING METHODS

    def drawInfo(self, surface):
        
        TURNFONT = pygame.font.Font('freesansbold.ttf', PTURN_FONTSIZE)
        STATFONT = pygame.font.Font('freesansbold.ttf', PSTAT_FONTSIZE)
        
        color_dict = {'red': RED, 'blue': BLUE}
        turn_text = self.name + "'s Turn"
        stats_text = ['Economy: ' + str(self.economy),
                      'Money: ' + str(self.money),
                      'Base HP: ' + str(self.bldgs[0].hp)]
        #Draw turn text
        turnSurf = TURNFONT.render(turn_text, True,
                                   color_dict[self.color])
        turnRect = turnSurf.get_rect()
        turnRect.topleft = (PTURN_OFFSETX, PTURN_OFFSETY)
        surface.blit(turnSurf, turnRect)

        #Draw stat text
        y_adjustment = 0
        for text in stats_text:
            statSurf = STATFONT.render(text, True, WHITE)
            statRect = statSurf.get_rect()
            statRect.topleft = (PSTAT_OFFSETX, PSTAT_OFFSETY + y_adjustment)
            surface.blit(statSurf, statRect)
            y_adjustment += 40
            

if __name__ == '__main__':

    print "Player Module for Dice Tactics"
    player = Player('josh', 'red', 3)
    print player.money
    print player.rollEconomyDice()
    print player.money
