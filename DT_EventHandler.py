## Event Handling module for Dice Tactics

import pygame, sys
from pygame.locals import *

def terminate():
    pygame.quit()
    sys.exit()
    
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event) # Put other KEYUP objects back in the event list

        
