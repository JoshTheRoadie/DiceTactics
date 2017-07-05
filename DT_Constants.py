#### Useful Constants for Dice Tactics


## DISPLAY VALUES
FPS = 30       # For controlling framerate

WINDOWWIDTH  = 640  # Width of the main window in pixels
WINDOWHEIGHT = 480  # Height of the main window in pixels


# BOARD VALUES
BOARDWIDTH  = 10    # Number of Tiles in a row on the Board
BOARDHEIGHT = 10    # Number of Tiles in a column on the Board
TILESIZE    = 32    # Width and Height of a Tile in pixels
GAPSIZE     = 2     # Size of the gap between Tiles in pixels
BRD_OFFSETX = 15    # Distance of Board from the left of the screen in pixels
BRD_OFFSETY = 15    # Distance of Board from the top of the screen in pixels

EMPTY_TILE = None   # Placeholder value for the Board.board matrix


## OFFSET VALUES FOR BUTTONS
BUYBUTTON_WIDTH   = 64   # Width of Buy Button in pixels
BUYBUTTON_HEIGHT  = 32   # Height of Buy Button in pixels
BUYBUTTON_OFFSETX = 15   # Offset from left of screen in pixels
BUYBUTTON_OFFSETY = 438  # Offset from top of screen in pixels

ENDBUTTON_WIDTH   = 64   # Width of End Turn Button in pixels
ENDBUTTON_HEIGHT  = 32   # Height of End Turn Button in pixels
ENDBUTTON_OFFSETX = 520  # Offset from left of screen in pixels
ENDBUTTON_OFFSETY = 438  # Offset from top of screen in pixels

BUTTON_FONTSIZE = 20 #Size of the font on the buttons

BUYOPTION_OFFSETX = 15 # Offset from left of screen in pixels
BUYOPTION_OFFSETY = 390 # Offset from bottom of screen in pixels

## GAME INFO DISPLAY CONSTANTS
PTURN_OFFSETX = 370  # Offset from left of screen in pixels
PTURN_OFFSETY = 15   # Offset from top of screen in pixels

PTURN_FONTSIZE = 30  # Size of font for player stats

PSTAT_OFFSETX = 370
PSTAT_OFFSETY = 65

PSTAT_FONTSIZE = 20

## PLAYER STARTING VALUES
STARTING_ECONOMY = 2  # Starting number of Economy Dice
STARTING_MONEY   = 0  # Starting money

## PIECE VALUES
BASEHP = 30  # The hit points of a player's base
ECONOMYCOST = 24  # Price of an Economy Die
TROOPCOSTS = {4:4,
              6:6,
              8:8,
              10:10,
              12:12,
              20:20} # Cost value for troops mapped to number of sides
TROOPMOVES = {4:4,
              6:3,
              8:3,
              10:2,
              12:2,
              20:2} # Move value for troops mapped to number of sides
TROOPVISION = {4:4,
               6:3,
               8:3,
               10:2,
               12:2,
               20:2} # How far a troop can see mapped to number of sides

## SPRITE NAMES
SPRITEKEYS = ['redbase', 'redd4', 'redd6', 'redd8', 'redd10', 'redd12',
               'redd20', 'darkredd4', 'darkredd6', 'darkredd8', 'darkredd10',
               'darkredd12', 'darkredd20', 'bluebase', 'blued4', 'blued6',
               'blued8', 'blued10', 'blued12', 'blued20', 'darkblued4',
               'darkblued6', 'darkblued8', 'darkblued10', 'darkblued12',
               'darkblued20', 'rock', 'tree'] # Key names for building a sprite dictionary
## COLOR DEFINITIONS
#          R    G    B  Color Definitions
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
BLUE    = (  0,   0, 255)
GREEN   = (  0, 255,   0)
YELLOW  = (255, 255,   0)
MAGENTA = (255,   0, 255)

## FONT COLORS
PTURN_TCOLOR = WHITE # Color of the font
PSTAT_TCOLOR = WHITE

