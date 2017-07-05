## Animations Module for Dice Tactics.
import pygame, sys, DT_EventHandler, DT_Pieces, DT_Board
from pygame.locals import *
from DT_Constants import TILESIZE

grassTile = pygame.image.load('grassTile.png')
trooplanding = pygame.image.load('trooplanding.png')
trooprising = pygame.image.load('trooprising.png')
atk_anim = pygame.image.load('atk_anim.png')
def_anim = pygame.image.load('def_anim.png')
parachute = pygame.image.load('parachute.png')
redd4 = pygame.image.load('redd6.png')
darkredd4 = pygame.image.load('darkredd6.png')



class Animation:

    def __init__(self, spritefile, fps):
        self.name = spritefile
        self.sheet = pygame.image.load(spritefile).convert()
        self.frames = self.sheet.get_rect().width / TILESIZE
        self.fps = fps

    def play(self, surface, pos):
        clock = pygame.time.Clock()
        posx, posy = pos
        background = surface.copy()
        for frame in range(0, self.frames):
            current_frame = (TILESIZE * frame, 0, TILESIZE, TILESIZE)
            surface.blit(background, (0, 0))
            surface.blit(self.sheet, pos, current_frame)
            pygame.display.update()
            clock.tick(self.fps)
        

# main doesn't work right now due to changing the animation functions. the
# functions work with the main game for now.
def main():
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((640, 480))

    BOARD = DT_Board.Board(10, 10, grassTile)
    troop = DT_Pieces.Troop([redd4, darkredd4], (5,5), 'red', 4)

    while True:
        SCREEN.fill((0,0,0))
        SCREEN.blit(grassTile, (300,300))
        atkDefAnimation(SCREEN, troop, BOARD, FPSCLOCK, 'def')
        troopAppearsAnima(SCREEN, troop, BOARD, FPSCLOCK, trooplanding)
        DT_EventHandler.checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick(60)
       
##def troopLandingAnimation(surface, spritesheet, frames,
##                          target_pos, troop,
##                          board, player, drawFunc, clock):
##    index_list = range(0, frames)
##    for index in index_list:
##        current_frame = (index * 32, 0, 32, 32)
##        drawFunc(surface, board, player)
##        surface.blit(troop.image[0], target_pos)
##        surface.blit(spritesheet, target_pos, current_frame)
##
##        DT_EventHandler.checkForQuit()
##        pygame.display.update()
##        clock.tick(30)

def troopLandingAnimation(surface, target_pos):
    spritesheet = pygame.image.load('trooplanding.png')
    frames = 10
    clock = pygame.time.Clock()
    temp_surf = surface.copy()
    for index in range(0, frames):
        current_frame = (index * 32, 0, 32, 32)
        surface.blit(temp_surf, (0, 0))
        surface.blit(spritesheet, target_pos, current_frame)

        DT_EventHandler.checkForQuit()
        pygame.display.update()
        clock.tick(30)

def placeTroopAnimation(surface, troop, target_pos,
                        board, player, drawFunc, clock):
    targetx, targety = target_pos
    for new_y in range(-32, targety+1, 3):
        drawFunc(surface, board, player)
        surface.blit(parachute, (targetx, new_y - 29))
        surface.blit(troop.image[0], (targetx, new_y))
        DT_EventHandler.checkForQuit()
        pygame.display.update()
        clock.tick(60)
    troopLandingAnimation(surface, target_pos)
    
##def placeTroopAnimation(surface, troop, target_pos,
##                        board, player, drawFunc, clock):
##    targetx, targety = target_pos
##    for new_y in range(-32, targety+1, 3):
##        drawFunc(surface, board, player)
##        surface.blit(parachute, (targetx, new_y - 29))
##        surface.blit(troop.image[0], (targetx, new_y))
##        DT_EventHandler.checkForQuit()
##        pygame.display.update()
##        clock.tick(60)
##    troopLandingAnimation(surface, trooplanding, 10,
##                          target_pos, troop, board,
##                          player, drawFunc, clock)
    

def troopAppearsAnima(surface, troop, board, clock, spritesheet):
    temp_surf = surface.copy()
    for index in range(0, 10):
        surface.fill((0,0,0))
        surface.blit(temp_surf, (0,0))

        pygame.display.update()
        clock.tick(10)

def atkDefAnimation(surface, troop, board, clock, typeflag):
    if typeflag == 'atk':
        spritesheet = atk_anim
    else:
        spritesheet = def_anim
    frames = 5
    boxx, boxy = troop.loc
    target_pos = board.leftTopCornerPixel(boxx, boxy)
    for index in range(0, frames):
        current_frame = (index * 32, 0, 32, 32)
        surface.blit(troop.image[0], target_pos)
        surface.blit(spritesheet, target_pos, current_frame)

        pygame.display.update()
        clock.tick(8)

if __name__ == '__main__':
    pygame.init()
    SCREEN = pygame.display.set_mode((640, 480))
    BOARD = DT_Board.Board(10,10, grassTile)
    anima = Animation('trooprising.png', 12)
    while True:
        BOARD.draw(SCREEN)
        anima.play(SCREEN, (100, 100))
        DT_EventHandler.checkForQuit()
        pygame.display.update()
        
