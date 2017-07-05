## Game Piece module for Dice Tactics

import pygame, DiceRoller
from DT_Constants import *
class Piece:
    ''' Ancestor class for all of the game pieces in Dice Tactics. '''

    def __init__(self, image_name, loc):
        self.image = image_name
        self.loc = loc

    def draw(self, surface, x, y):
        '''Draws the image in self.image to the screen at (x, y) where
        x and y are measured in pixels.'''
        surface.blit(self.image, (x, y))


class Obstacle(Piece):
    '''Represents obstacles (rocks, trees, etc) on the game board.'''

    def __init__(self, image_name, loc):
        Piece.__init__(self, image_name, loc)


class Troop(Piece):
    '''Represents a player's troops (dice) on the game board.'''
    
    def __init__(self, image_list, loc, color, sides):
        '''When creating a Troop piece, the image should be a list of two
        images instead a single image'''
        Piece.__init__(self, image_list, loc)
        self.color = color
        self.sides = sides
        self.move = TROOPMOVES[sides]
        self.vision = TROOPVISION[sides]
        self.has_moved = True

    def findValidMoves(self, board):
        '''Checks all possible locations on the board within the troop's
        self.move range to see if it is a possible move for the troop.
        Returns -> list of valid move locations in (x, y) form.'''
        x, y = self.loc  #x, y of selected troop
        valid_moves = []

        #Dictionary for checking if a move is blocked by another piece
        path_blocked = {'right': False,
                        'left': False,
                        'down': False,
                        'up': False}

        #Loop for determining moves
        for step in range(1, self.move + 1):
            #Dictionary for checking each direction
            step_locs = {'right': (x + step, y),
                         'down': (x, y + step),
                         'left': (x - step, y),
                         'up': (x, y - step)}

            #Loops through step_loc dictionary to check each direction.
            for direction in step_locs.keys():
                #Check that loc exists on the board.
                if board.validateLoc(step_locs[direction]):
                    #Check that the tile is empty and the path is not blocked by another piece.
                    if board.tileIsEmpty(step_locs[direction]) \
                       and not path_blocked[direction]:
                        valid_moves.append(step_locs[direction]) #Valid move added to list.
                    #Check if the tile is occupied by an opponent's Troop piece
                    elif isinstance(board.getItem(step_locs[direction]), Troop) \
                         and not path_blocked[direction] \
                         and board.getItem(step_locs[direction]).color != self.color:
                        valid_moves.append(step_locs[direction])
                        path_blocked[direction] = True
                    #The tile is occupied or another piece is blocking the calling troop.
                    else:
                        path_blocked[direction] = True

        return valid_moves

    def findAdjacentBuildings(self, board):
        x, y = self.loc
        targets = []
        for step in [-1, 1]:
            possible_locs = [(x + step, y), (x, y + step)]
            for loc in possible_locs:
                if board.validateLoc(loc) and not board.tileIsEmpty(loc):
                    item = board.getItem(loc)
                    if isinstance(item, Building) and item.color != self.color:
                        targets.append(loc)
        return targets

    def highlightMoves(self, surface, board, valid_moves):
        '''Draws square outlines around the tiles with locs found in the list: valid_moves'''
        for move_loc in valid_moves:
            boxx, boxy = move_loc
            left, top = board.leftTopCornerPixel(boxx, boxy)
            pygame.draw.rect(surface, GREEN, (left, top, TILESIZE, TILESIZE), 2)

    def moveTo(self, board, new_loc):
        '''Moves the troop from its current loc to the new_loc on the board.
        This updates the troop.loc and the Board.board.'''
        old_loc = self.loc
        self.loc = new_loc
        board.placeItem(board.getItem(old_loc), new_loc)
        board.removeItem(old_loc)
        self.has_moved = True

    def attack(self, defender):
        attack_roll = DiceRoller.roll(self.sides)
        defend_roll = DiceRoller.roll(defender.sides)
        if attack_roll > defend_roll:
            return (attack_roll, defend_roll, True)
        else:
            return (attack_roll, defend_roll, False)

    def attackBuilding(self, building):
        attack_roll = DiceRoller.roll(self.sides)
        building.hp = building.hp - attack_roll
        return attack_roll

    def findVisibleTiles(self, board):
        '''This finds the locs of all tiles that are within the range
        of a troop's vision.'''
        startx, starty = self.loc
        visible_tiles = []
        for x_adjust in range(-self.vision, self.vision + 1):
            currentx = startx + x_adjust
            y_max = self.vision - abs(x_adjust)
            for y_adjust in range(-y_max, y_max + 1):
                currenty = starty + y_adjust
                if board.validateLoc((currentx, currenty)):
                    visible_tiles.append((currentx, currenty))
        return visible_tiles
    
    def draw(self, surface, x, y):
        '''Overrides the .draw method of the ancestor class: Piece.  This draws
        one of two different images for the troop based on the .has_moved
        attribute value.'''
        if self.has_moved:
            surface.blit(self.image[1], (x, y))
        else:
            surface.blit(self.image[0], (x, y))
        
class Building(Piece):
    '''Represents a player's building pieces such as the Base'''

    def __init__(self, image_name, color, loc, hp):
        Piece.__init__(self, image_name, loc)
        self.color = color
        self.hp = hp

    def damaged(self, amount):
        self.hp = self.hp - amount

    def findPlacementLocs(self, board):
        x, y = self.loc
        valid_placements = []
        for step in [-1, 1]:
            possible_locs = [(x + step, y), (x, y + step)]
            for loc in possible_locs:
                if board.validateLoc(loc) and board.tileIsEmpty(loc):
                    valid_placements.append(loc)
        return valid_placements

    def highlightPlacements(self, surface, board, valid_placements):
        '''Draws square outlines around the tiles with locs found in the list: valid_moves'''
        for loc in valid_placements:
            boxx, boxy = loc
            left, top = board.leftTopCornerPixel(boxx, boxy)
            pygame.draw.rect(surface, YELLOW, (left, top, TILESIZE, TILESIZE), 2)

            
if __name__ == '__main__':

    print 'Dice Tactics Pieces Mudule.'
    


