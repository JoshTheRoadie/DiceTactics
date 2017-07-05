#### Dice Tactics GUI and Graphics Module
#### Uses the pygame framework.

import pygame, sys, DT_Player
from pygame.locals import *
from DT_Constants import *

# Game Constants
##FPS = 30
##WINDOWWIDTH = 640
##WINDOWHEIGHT = 480
##BOARDWIDTH = 10
##BOARDHEIGHT = 10
##BOXSIZE = 32
##GAPSIZE = 2
##XMARGIN = 15
##YMARGIN = 15
##
##EMPTY_TILE = None
##
###          R    G    B  Color Definitions
##BLACK  = (  0,   0,   0)
##WHITE  = (255, 255, 255)
##RED    = (255,   0,   0)
##BLUE   = (  0,   0, 255)
##GREEN  = (  0, 255,   0)
##YELLOW = (255, 255,   0)


def main():
    global FPSCLOCK, SCREEN
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    grassTile = pygame.image.load('grassTile.png')
    mousex = 0
    mousey = 0
    mouseClicked = False
    pygame.display.set_caption('Dice Tactics')

    BOARD = create_board()

    player1 = DT_Player.Player('Player 1', 2)
    player2 = DT_Player.Player('Player 2', 2)

    player1.troops = [(0,1), (2,3), (5,7)]
    player2.troops = [(1,1), (8,9), (6,4)]

    players = [player1, player2]

    # BUTTON SIZE AND PLACEMENT CHECK
    buyoffx = 15
    buyoffy = 438
    bw = 64
    bh = 32

    endoffx = 551
    endoffy = 438
    ew = 64
    eh = 32
    
    while True:
        
##        draw_board(BOARD)
        draw_board(BOARD, grassTile)
        drawUnitsOnBoard(players)
        pygame.draw.rect(SCREEN, RED, (buyoffx, buyoffy, bw, bh)) #buy button placement
        pygame.draw.rect(SCREEN, YELLOW, (endoffx, endoffy, ew, eh)) #end button placement
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
                
        highlightBox(mousex, mousey)
        if mouseClicked:
            changeColorOnClick(mousex, mousey)
            mouseClicked = False
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def create_board():
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(EMPTY_TILE)
        board.append(column)
    return board

def leftTopBoxCoords(boxx, boxy):
    left = boxx * (TILESIZE + GAPSIZE) + BRD_OFFSETX
    top = boxy * (TILESIZE + GAPSIZE) + BRD_OFFSETY
    return (left, top)

##def draw_board(board):
##    for boxx in range(BOARDWIDTH):
##        for boxy in range(BOARDHEIGHT):
##            left, top = leftTopBoxCoords(boxx, boxy)
##            pygame.draw.rect(SCREEN, WHITE, (left, top, BOXSIZE, BOXSIZE))

def draw_board(board, tile):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopBoxCoords(boxx, boxy)
            SCREEN.blit(tile, (left, top))
            
def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopBoxCoords(boxx, boxy)
            boxRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def highlightBox(x, y):
    boxx, boxy = getBoxAtPixel(x, y)
    if boxx != None and boxy != None:
        left, top = leftTopBoxCoords(boxx, boxy)
        pygame.draw.rect(SCREEN, GREEN, (left, top, TILESIZE, TILESIZE))

def changeColorOnClick(x, y):
    boxx, boxy = getBoxAtPixel(x, y)
    if boxx != None and boxy != None:
        left, top = leftTopBoxCoords(boxx, boxy)
        pygame.draw.rect(SCREEN, YELLOW, (left, top, TILESIZE, TILESIZE))

def drawUnitsOnBoard(players_list):
    for player in players_list:
        for troop in player.troops:
            x, y = troop
            left, top = leftTopBoxCoords(x, y)
            if player.name == 'Player 1':
                pygame.draw.rect(SCREEN, RED, (left, top, TILESIZE, TILESIZE))
            else:
                pygame.draw.rect(SCREEN, BLUE, (left, top, TILESIZE, TILESIZE))
                
if __name__ == '__main__':
    main()
