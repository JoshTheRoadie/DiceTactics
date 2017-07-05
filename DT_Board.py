# Board Module for Dice Tactics.

import pygame, sys
from pygame.locals import *
from DT_Constants import *

EMPTYTILE = EMPTY_TILE
        
class Board:
    '''A class for creating and managing a 2-dimensional list that
    represents a game board assembled from square tiles.'''

    def __init__(self, width, height, tile, obstacle_list = None):
        self.width = width     #number of rows
        self.height = height   #number of columns
        self.tile = tile       #the tile image used to draw the board
        self.obstacles = obstacle_list #optional list of DT_Pieces.Obstacles objects

        #Create board data structure
        board = []
        for x in range(width):
            column = []
            for y in range(height):
                column.append(EMPTYTILE)
            board.append(column)

        self.board = board

        #Place obstacles in the board data structure if a list of obstacles
        #was provided.
        if self.obstacles:
            for obstacle in self.obstacles:
                self.placeItem(obstacle, obstacle.loc)
            
## BOARD AND ITEM MANIPULATION METHODS
        
    def validateLoc(self, loc):
        '''Return True if loc is within the size of the board
        and False otherwise.'''
        x, y = loc
        if x < 0 or y < 0:
            return False
        if x >= len(self.board):
            return False
        for column in self.board:
            if y >= len(column):
                return False
        return True
    
    def getItem(self, loc):
        '''Return the element stored at loc in the board. Does NOT remove
        the element from the board.'''
        x, y = loc
        return self.board[x][y]

    def placeItem(self, item, loc):
        '''Places the item into the board data structure at loc.'''
        x, y = loc
        self.board[x][y] = item

    def removeItem(self, loc, replacement = EMPTYTILE):
        '''Removes(replaces) the element at the loc in the board. The
        replacement can be anything, but defaults to the EMPTYTILE.'''
        x, y = loc
        self.board[x][y] = replacement

    def tileIsEmpty(self, loc):
        '''Returns True if the element at loc in the board is the
        placeholder value: EMPTYTILE and False otherwise.'''
        x, y = loc
        if self.board[x][y] == EMPTYTILE:
            return True
        else:
            return False

    def findItem(self, item):
        '''Returns the loc of the item in the board or (None,None) if
        the item is not in the board.'''
        for x in range(self.width):
            for y in range(self.height):
                if self.board[x][y] == item:
                    return (x, y)
        return (None, None)

    def updateBoard(self, player_list):
        for player in player_list:
            player.updatePiecesOnBoard(self)
            
    def printBoard(self):
        '''Prints the board to the CLI.'''
        for x in range(self.width):
            print
            for y in range(self.height):
                print str(self.board[x][y]),
        print

## PYGAME INTERACTION METHODS

    def leftTopCornerPixel(self, boxx, boxy):
        '''Returns the (x,y) pixel coordinates of the tile at
        board[x][y].'''
        left = boxx * (TILESIZE + GAPSIZE) + BRD_OFFSETX
        top = boxy * (TILESIZE + GAPSIZE) + BRD_OFFSETY
        return (left, top)

    def getTileAtPixel(self, x, y):
        '''Returns the (x,y) board index coordinates if the pixel coordinates
        passed are within a tile of the board.  Returns (None,None) if the
        passed coordinates are not within a tile.'''
        for boxx in range(self.width):
            for boxy in range(self.height):
                left, top = self.leftTopCornerPixel(boxx, boxy)
                boxRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
                if boxRect.collidepoint(x, y):
                    return (boxx, boxy)
        return (None, None)
    
    def draw(self, surface):
        '''Blits the sprite passed in tile to the display surface for
        each tile in the board.'''
        for boxx in range(self.width):
            for boxy in range(self.height):
                left, top = self.leftTopCornerPixel(boxx, boxy)
                surface.blit(self.tile, (left, top))

    def drawPieces(self, surface):
        '''Iterates through the entire board and draws the pieces it finds
        to the display surface.'''
        for boxx in range(self.width):
            for boxy in range(self.height):
                piece = self.getItem((boxx, boxy))
                if piece != EMPTY_TILE:
                    left, top = self.leftTopCornerPixel(boxx, boxy)
                    piece.draw(surface, left, top)
        
##    def drawBoxes(self, surface, color=WHITE):
##        for boxx in range(BOARDWIDTH):
##            for boxy in range(BOARDHEIGHT):
##                left, top = self.leftTopCornerPixel(boxx, boxy)
##                pygame.draw.rect(SCREEN, color, (left, top, TILESIZE, TILESIZE))



class Button:

    def __init__(self, text, font, textcolor, bgcolor, offsetx, offsety):
        self.text = text
        self.surf = font.render(text, True, textcolor, bgcolor)
        self.rect = self.surf.get_rect()
        self.rect.topleft = (offsetx, offsety)
        
if __name__ == '__main__':
    print 'Board Module for Dice Tactics'
