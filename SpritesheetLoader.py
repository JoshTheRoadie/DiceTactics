## PYGAME BASIC SETUP TEMPLATE

import pygame, sys, random, DT_EventHandler
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

econ_dice = pygame.image.load('economydice.png')

def main():
    global FPSCLOCK
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    while True:
        animateSpritesheet(SCREEN, econ_dice)
        DT_EventHandler.checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    

def animateSpritesheet(surface, spritesheet):
    index_list = [0,1,2,3,4,5]
    target_pos = surface.get_rect().center
    wait_times = range(0, 400, 20)
    for delay in wait_times:
        sprite_index = random.choice(index_list)
        current_frame = sprite_index * 32
        surface.blit(spritesheet, target_pos, (current_frame, 0, 32, 32))
        DT_EventHandler.checkForQuit()        
        pygame.display.update()
        pygame.time.wait(delay)
        FPSCLOCK.tick(FPS)



if __name__ == '__main__':
    main()
