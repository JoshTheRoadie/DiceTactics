## Dice Tactics Game
## Version 0.3.1
## By: Joshua McCready and Sean Thornton
##
## New:
#   - Completely re-coded the "clicked on a troop" portion of the event
#       handling loop for clarity and UI cleanliness.
#   - Text indicators added that let the player know the reason they
#       cannot buy troops or economy dice (not enough money, or not enough
#       space).
#   - Now displays the economy dice roll for the player on their turn. Does
#       not yet work in sub-loops like troopEVent() and buyButtonEvent()
#   - Added a simple animation when buying a troop.  The troop now falls into
#       place.  Had to import a new module for this: DT_Animations
#
## Known Bugs:
#   - FIXED!!! Doesn't check to see if all adjacent tiles around a base are
#       occupied before selecting a troop to buy. Troop can still be bought,
#       but it crashes(hangs, really) the game.
#

import pygame, sys, DT_Board, DT_Pieces, DT_Player, DT_EventHandler
import DT_Animations as anima
from pygame.locals import *
from DT_Constants import *

def main():
    global FPSCLOCK, SCREEN, BUTTONLIST, PLAYERLIST, PIECESPRITES, PTURN_FONT, \
           PSTAT_FONT

    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()

    #Create Font objects
    BUTTON_FONT = pygame.font.Font('freesansbold.ttf', BUTTON_FONTSIZE)
    PTURN_FONT = pygame.font.Font('freesansbold.ttf', PTURN_FONTSIZE)
    PSTAT_FONT = pygame.font.Font('freesansbold.ttf', PSTAT_FONTSIZE)
    
    #Load sprites
    BOARDTILE = pygame.image.load('grassTile.png')
    ECONOMYSPRITE = pygame.image.load('economydice.png')
    PIECESPRITES = loadSprites(SPRITEKEYS)

    #Put obstacles on the board
    rockTile = PIECESPRITES['rock']
    obstacle_list   = [DT_Pieces.Obstacle(rockTile, (3,4)),
                       DT_Pieces.Obstacle(rockTile, (4,4)),
                       DT_Pieces.Obstacle(rockTile, (5,5)),
                       DT_Pieces.Obstacle(rockTile, (6,5))]

    #Create the Board object
    BOARD = DT_Board.Board(BOARDWIDTH, BOARDHEIGHT, BOARDTILE, obstacle_list)
    
    #Make player bases
    player1_base = DT_Pieces.Building(PIECESPRITES['redbase'], 'red',
                                      (4,1), 30)
    player2_base = DT_Pieces.Building(PIECESPRITES['bluebase'], 'blue',
                                      (5,8), 30)

    #Make players and add bases
    player1 = DT_Player.Player('Josh', 'red', STARTING_ECONOMY)
    player1.addBuildingList([player1_base])

    player2 = DT_Player.Player('Sean', 'blue', STARTING_ECONOMY)
    player2.addBuildingList([player2_base])

    PLAYERLIST = [player1, player2]

    #Update the Board data structure with player pieces
    for player in PLAYERLIST:
        player.updatePiecesOnBoard(BOARD)

    #Make the buttons
    buyButton = DT_Board.Button('BUY PIECE', BUTTON_FONT, YELLOW, RED,
                                BUYBUTTON_OFFSETX, BUYBUTTON_OFFSETY)
    endButton = DT_Board.Button('END TURN', BUTTON_FONT, WHITE, BLUE,
                                ENDBUTTON_OFFSETX, ENDBUTTON_OFFSETY)
    BUTTONLIST = [buyButton, endButton]

    #Set up some game variables
    SCREEN = pygame.display.set_mode((WINDOWWIDTH,  WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    mouseClicked = False

    playerturn = 0
    rolled_dice = []
    has_rolled_economy = False
    
    while True:

        current_player = PLAYERLIST[playerturn % 2]
        drawMainGameScreen(SCREEN, BOARD, current_player)

        #Roll economy dice if the player hasn't yet
        if not has_rolled_economy:
            rolled_dice = current_player.rollEconomyDice()
            has_rolled_economy = True
        else:
            drawEconomyRoll(rolled_dice, ECONOMYSPRITE)
            
        #Handle Events
        DT_EventHandler.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if mouseClicked:

            #Starts the troop event handler
            if troopClicked(BOARD, current_player, mousex, mousey):
                troop = BOARD.getItem(BOARD.getTileAtPixel(mousex, mousey))
                troopEvent(BOARD, troop, current_player)
                mouseClicked = False

            #Starts the buy event handler
            elif buyButton.rect.collidepoint(mousex, mousey) \
                 or baseClicked(BOARD, current_player, mousex, mousey):
                buyButtonEvent(BOARD, current_player, buyButton)
                mouseClicked = False

            #Ends current player's turn and increments to next player
            elif endButton.rect.collidepoint(mousex, mousey):
                playerturn += 1
                has_rolled_economy = False
                for player in PLAYERLIST:
                    for troop in player.troops:
                        troop.has_moved = False
                mouseClicked = False
                
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
## FUNCTIONS

def troopClicked(board, player, mousex, mousey):
    '''Returns True if the player clicked on one of their own troops,
    otherwise returns False.'''
    boxx, boxy = board.getTileAtPixel(mousex, mousey)
    if boxx != None and boxy != None:
        item = board.getItem((boxx, boxy))
        if isinstance(item, DT_Pieces.Troop) and \
           item in player.troops and not item.has_moved:
            return True
        else:
            return False

def baseClicked(board, player, mousex, mousey):
    '''Returns True if a player clicked on their own base, otherwise
    returns False.'''
    boxx, boxy = board.getTileAtPixel(mousex, mousey)
    if boxx != None and boxy != None:
        item = board.getItem((boxx, boxy))
        if isinstance(item, DT_Pieces.Building) and \
           item.loc == player.bldgs[0].loc:
            return True
    else:
        return False

def troopEvent(board, troop, player):
    '''Handles all possible events if a troop owned by the current player
    is clicked.'''
    mousex = 0
    mousey = 0
    mouseClicked = False

    #Finds all possible locs for the troop. Move locs, enemy locs, and
    #opponent building locs.
    valid_selections = troop.findValidMoves(board) \
                       + troop.findAdjacentBuildings(board)
    while True:
        drawMainGameScreen(SCREEN, board, player)
        troop.highlightMoves(SCREEN, board, valid_selections)
        
        DT_EventHandler.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if mouseClicked:
            boxx, boxy = board.getTileAtPixel(mousex, mousey)
            if (boxx, boxy) == troop.loc: return #deselect troop
            
            if (boxx, boxy) in valid_selections:
                # Move to selected empty tile
                if board.tileIsEmpty((boxx, boxy)):
                    troop.moveTo(board, (boxx, boxy))
                    # Now check for buildings to attack.
                    adj_bldgs = troop.findAdjacentBuildings(board)
                    if adj_bldgs:
                        attackBldgAfterMove(board, player, troop, adj_bldgs)
                    return

                # Attack enemy troop
                elif isinstance(board.getItem((boxx,boxy)),
                              DT_Pieces.Troop):
                    attackTroop(board, player, troop, board.getItem((boxx,boxy)))
                    return

                # Attack enemy building
                elif isinstance(board.getItem((boxx, boxy)),
                                DT_Pieces.Building):
                    attackBldg(board, player, troop, board.getItem((boxx, boxy)))
                    return
            

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def attackTroop(board, player, attacker, defender):
    attack_roll, defend_roll, attack_won = attacker.attack(defender)
    drawAttackRolls(board, attacker, defender, attack_roll, defend_roll)
    if attack_won:
        attacker.moveTo(board, defender.loc)
        for opponent in PLAYERLIST:
            if opponent != player:
                opponent.troops.remove(defender)
                return
    else:
        board.removeItem(attacker.loc)
        player.troops.remove(attacker)
        return

def attackBldg(board, player, troop, building):
    attack_roll = troop.attackBuilding(building)
    drawBuildingDamage(board, building, attack_roll)
    troop.has_moved = True
    if building.hp <= 0:
        gameOverScreen(player)

def attackBldgAfterMove(board, player, troop, adjacent_buildings):
    mousex = 0
    mousey = 0
    mouseClicked = False
    while True:
        drawMainGameScreen(SCREEN, board, player)
        troop.highlightMoves(SCREEN, board, adjacent_buildings)
        
        DT_EventHandler.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        if mouseClicked:
            boxx, boxy = board.getTileAtPixel(mousex, mousey)
            if (boxx, boxy) == troop.loc:
                return #deselect troop
            
            elif (boxx, boxy) in adjacent_buildings:
                attackBldg(board, player, troop, board.getItem((boxx, boxy)))
                return
            mouseClicked = False

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def drawAttackRolls(board, attacker, defender, attack_roll, defend_roll):
    '''Draws the outcomes of the attack and defend rolls on the screen over
    the appropriate troop.'''
    rollFont = pygame.font.Font('freesansbold.ttf', 30)
    atk_roll_surf = rollFont.render(str(attack_roll), True, YELLOW)
    atk_roll_rect = atk_roll_surf.get_rect()
    a_boxx, a_boxy = attacker.loc
    atk_roll_rect.topleft = board.leftTopCornerPixel(a_boxx, a_boxy)
    
    def_roll_surf = rollFont.render(str(defend_roll), True, YELLOW)
    def_roll_rect = def_roll_surf.get_rect()
    d_boxx, d_boxy = defender.loc
    def_roll_rect.topleft = board.leftTopCornerPixel(d_boxx, d_boxy)

    SCREEN.blit(atk_roll_surf, atk_roll_rect)
    SCREEN.blit(def_roll_surf, def_roll_rect)
    pygame.display.update()
    pygame.time.wait(1500)
    
def drawBuildingDamage(board, building, damage):
    '''Draws the outcome of the attack roll against a building over the
    target building.'''
    dmgFont = pygame.font.Font('freesansbold.ttf', 30)
    dmg_surf = dmgFont.render(str(damage), True, YELLOW)
    dmg_rect = dmg_surf.get_rect()
    boxx, boxy = building.loc
    dmg_rect.topleft = board.leftTopCornerPixel(boxx, boxy)

    SCREEN.blit(dmg_surf, dmg_rect)
    pygame.display.update()
    pygame.time.wait(1500)
    
def buyButtonEvent(board, player, buybutton):
    '''Handles events once the buy button or the current player's base
    is clicked.'''
    mousex = 0
    mousey = 0
    mouseClicked = False
    while True:
        drawMainGameScreen(SCREEN, board, player)
        buy_options = makeBuyOptionButtons()
        drawButtons(buy_options) # Draws the Buy Option buttons to the screen

        DT_EventHandler.checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                for option in buy_options:
                    # Check to see if one of the buy options was clicked.
                    if option.rect.collidepoint(mousex, mousey):
                        selection = option.text
                        mouseClicked = True

                    # If the same base or the buy button is clicked again,
                    # Exit out of the buy option handler.
                    elif baseClicked(board, player, mousex, mousey):
                        return

                    elif buybutton.rect.collidepoint(mousex, mousey):
                        return

        if mouseClicked:
            # Cheek if the player wants an Economy Die
            if selection == 'ECON':
                if ECONOMYCOST > player.money:
                    drawBuyAlert('You cannot afford an economy die.')
                    return
                else:
                    player.economy = player.economy + 1
                    player.money = player.money - ECONOMYCOST
                    return
                
            # If the cost of the option collected is greater than the
            # player's money, exit back to the main program.
            if TROOPCOSTS[int(selection)] > player.money:
                drawBuyAlert('You cannot afford that troop.')
                return

            # if Economy Die was not selected and there are no open tiles
            # adjacent to the base, exit back to main program.
            if not player.bldgs[0].findPlacementLocs(board):
                drawBuyAlert('There are no open tiles near your base.')
                return
            
            # Otherwise buy the troop and place it on the board.
            new_troop = player.buyTroop(PIECESPRITES, int(selection))
            valid_locs = player.bldgs[0].findPlacementLocs(board)
            player_choosing = True
            while player_choosing:
                drawMainGameScreen(SCREEN, board, player)
                player.bldgs[0].highlightPlacements(SCREEN, board, valid_locs)

                DT_EventHandler.checkForQuit()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        choice = board.getTileAtPixel(mousex, mousey)
                        if choice in valid_locs:
                            #trying animation here
                            targetx, targety = choice
                            target_pos = board.leftTopCornerPixel(targetx, targety)
                            anima.placeTroopAnimation(SCREEN, new_troop,
                                                      target_pos,
                                                      board, player,
                                                      drawMainGameScreen,
                                                      FPSCLOCK)
                            #end attempt here
                            board.placeItem(new_troop, choice)
                            new_troop.loc = choice
                            return

                pygame.display.update()
                FPSCLOCK.tick(FPS)
            
            mouseClicked = False
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawBuyAlert(text):
    '''Draws the passed text just above the Buy Option Buttons. This
    is used for alerting the player why they can't buy something.'''
    infoFont = pygame.font.Font('freesansbold.ttf', 12)
    info_surf = infoFont.render(text, True, WHITE)
    info_rect = info_surf.get_rect()
    info_rect.topleft = (BUYOPTION_OFFSETX, BUYOPTION_OFFSETY - 18)
    SCREEN.blit(info_surf, info_rect)
    pygame.display.update()
    pygame.time.wait(1500)
    
def makeBuyOptionButtons():
    '''Creates a list of Button() objects that are used for buying
    troops and economy die.'''
    buy_options = [' 4', ' 6', ' 8', ' 10', ' 12', ' 20', 'ECON']
    buy_option_buttons = []
    next_button_offsetx = BUYOPTION_OFFSETX
    BUYOPTION_FONT = pygame.font.Font('freesansbold.ttf', 20)
    for option in buy_options:
        button = DT_Board.Button(option, BUYOPTION_FONT, BLUE, WHITE,
                                 next_button_offsetx,
                                 BUYOPTION_OFFSETY)
        buy_option_buttons.append(button)
        next_button_offsetx = next_button_offsetx + 40
    return buy_option_buttons
        
def loadSprites(keylist):
    '''Loads sprites files using the names in the keylist and
    puts the sprites in a dictionary referenced by the keys from
    keylist.'''
    sprite_dict = {}
    for key in keylist:
        sprite = pygame.image.load('%s.png' % key)
        sprite_dict[key] = sprite
    return sprite_dict

def drawButtons(button_list):
    '''Draws button objects to the screen.'''
    for button in button_list:
        SCREEN.blit(button.surf, button.rect)

def drawPlayerTurnText(player):
    '''Draws the current player's name to the screen to indicate
    whose turn it is.'''
    text = player.name + "'s Turn"
    textSurf = PTURN_FONT.render(text, True, PTURN_TCOLOR)
    textRect = textSurf.get_rect()
    textRect.topleft = (PTURN_OFFSETX, PTURN_OFFSETY)
    SCREEN.blit(textSurf, textRect)

def drawPlayerStatsText(player):
    '''Draws the Player's stats to the screen.'''
    econ_text =  'Economy: ' + str(player.economy)
    money_text = 'Money: ' + str(player.money)
    basehp_text = 'Base HP: ' + str(player.bldgs[0].hp)
    textlist = [econ_text, money_text, basehp_text]
    y_adjustment = 0
    for text in textlist:
        textSurf = PSTAT_FONT.render(text, True, PSTAT_TCOLOR)
        textRect = textSurf.get_rect()
        textRect.topleft = (PSTAT_OFFSETX, PSTAT_OFFSETY + y_adjustment)
        SCREEN.blit(textSurf, textRect)
        y_adjustment += 40

def drawEconomyRoll(rolls, spritesheet):
    target_posx = PSTAT_OFFSETX
    target_posy = 200
    posx_adjust = 0
    i = 1
    for roll in rolls:
        current_frame = (roll - 1) * TILESIZE
        frame_rect = (current_frame, 0, TILESIZE, TILESIZE)
        target_pos = (PSTAT_OFFSETX + posx_adjust, target_posy)
        SCREEN.blit(spritesheet, target_pos, frame_rect)
        posx_adjust = posx_adjust + GAPSIZE + TILESIZE
        i += 1
    
def gameOverScreen(player):
    '''Displays the winner's name when the game has ended.'''
    winner_text = player.name + ' has won!'
    text_obj = pygame.font.Font('freesansbold.ttf', 40)
    textSurf = text_obj.render(winner_text, True, GREEN)
    textRect = textSurf.get_rect()
    textRect.center = SCREEN.get_rect().center
    while True:
        SCREEN.fill(BLACK)
        SCREEN.blit(textSurf, textRect)

        DT_EventHandler.checkForQuit()
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawMainGameScreen(surface, board, player):
    '''Calls multiple functions to draw all main UI elements to the screen.'''
    surface.fill(BLACK)
    board.draw(SCREEN)
    board.drawPieces(SCREEN)
    drawButtons(BUTTONLIST)
    drawPlayerTurnText(player)
    drawPlayerStatsText(player)

if __name__ == '__main__':
    main()
    
