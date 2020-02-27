"""
Constants for Alien Invaders

This module global constants for the game Alien Invaders. These constants need
to be used in the model, the view, and the controller. As these are spread
across multiple modules, we separate the constants into their own module.
This allows all modules to access them.

YuBin (Kayla) Heo, yh356
December 4th, 2018
"""
import introcs
import sys


### WINDOW CONSTANTS (all coordinates are in pixels) ###

#: the width of the game display
GAME_WIDTH  = 800
#: the height of the game display
GAME_HEIGHT = 700


### SHIP CONSTANTS ###

# the width of the ship
SHIP_WIDTH    = 44
# the height of the ship
SHIP_HEIGHT   = 44
# the distance of the (bottom of the) ship from the bottom of the screen
SHIP_BOTTOM   = 32
# The number of pixels to move the ship per update
SHIP_MOVEMENT = 5
# The number of lives a ship has
SHIP_LIVES    = 3

#<Extension: Animate the Aliens>
#SHIP_IMAGE = 'ship.png'
SHIP_IMAGE = 'ship-strip.png'

# The y-coordinate of the defensive line the ship is protecting
DEFENSE_LINE = 100
DEFENSE_LINE_COLOR = 'gray'


#<Extension: Defense Barriers>
### Defense Barriers CONSTANTS ###

# the width of an Defense Barriers
DEFENSE_BARRIERS_WIDTH   = 120
# the height of an Defense Barriers
DEFENSE_BARRIERS_HEIGHT  = 120
# the horizontal separation between Defense Barriers
DEFENSE_BARRIERS_SEP = 64
# fix Ration difference (actual height 120 - 70)
DEFENSE_BARRIERS_COLLIDES_GAP = 50
# Height of Defense Barriers
DEFENSE_BARRIERS_LINE = (DEFENSE_LINE + 2 + DEFENSE_BARRIERS_HEIGHT/2)
# Number of Defense Barriers (max 4)
DEFENSE_BARRIERS_NUM = 4
# Strength of Defense Barriers
DEFENSE_BARRIERS_FRAMES = 9


### ALIEN CONSTANTS ###

# the width of an alien
ALIEN_WIDTH   = 33
# the height of an alien
ALIEN_HEIGHT  = 33
# the horizontal separation between aliens
ALIEN_H_SEP   = 16
# the vertical separation between aliens
ALIEN_V_SEP   = 16
# the number of horizontal pixels to move an alien
ALIEN_H_WALK  = ALIEN_WIDTH // 4
# the number of vertical pixels to move an alien
ALIEN_V_WALK  = ALIEN_HEIGHT // 2
# The distance of the top alien from the top of the window
ALIEN_CEILING = 100
# the number of rows of aliens, in range 1..10
ALIEN_ROWS     = 5
# the number of aliens per row
ALIENS_IN_ROW  = 12
# the image files for the aliens (bottom to top)


#<Extension: Animate the Aliens>
#ALIEN_IMAGES   = ('alien1.png','alien2.png','alien3.png')
ALIEN_IMAGES   = ('alien-strip1.png','alien-strip2.png','alien-strip3.png')

# the number of seconds (0 < float <= 1) between alien steps
ALIEN_SPEED = 1.0
# score for destroying aliens
ALIEN_SCORE = (10, 20, 40)
# ratio of speed of aliens
ALIEN_SPEED_RATIO = 0.5

# max ALIEN_ROWS
ALIEN_ROWS_MAX = 10
# max ALIENS_IN_ROW
ALIENS_IN_ROW_MAX = 15


### BOLT CONSTANTS ###

# the width of a laser bolt
BOLT_WIDTH  = 4
# the height of a laser bolt
BOLT_HEIGHT = 16
# the number of pixels to move the bolt per update
BOLT_SPEED  = 10
# the number of ALIEN STEPS (not frames) between bolts
BOLT_RATE   = 5
# color of bolt
BOLT_COLOR = 'red'


### GAME CONSTANTS ###

# <Extension: Intro Animation>
STATE_INTRO = -1
# state before the game has started
STATE_INACTIVE = 0
# state when we are initializing a new wave
STATE_NEWWAVE  = 1
# state when the wave is activated and in play
STATE_ACTIVE   = 2
# state when we are paused between lives
STATE_PAUSED   = 3
# state when we restoring a destroyed ship
STATE_CONTINUE = 4
#: state when the game is complete (won or lost)
STATE_COMPLETE = 5

#<Extension: Multiple Waves>
# text to inform the player how to continue
GAME_TEXT_CONTINUE = "Press 'C' to Continue"
# text for labeling score
GAME_TEXT_SCORE = "Score: "
# text for labeling lives
GAME_TEXT_LIVES = "Lives: "
# text for inform victory
GAME_TEXT_GAMECLEAR = "WIN!"
# text for labeling level
GAME_TEXT_LEVEL = "Level "
# text for inform lost
GAME_TEXT_GAMEOVER = "GAME OVER"
# line color of text
GAME_TEXT_COLOR = [1,1,1,1]
# color of text for continue
GAME_TEXT_CONTINUE_COLOR = [1,0,0,1]
# fill color of text
GAME_TEXT_FILL_COLOR = [0,0,0,1]
# color of text for score
GAME_TEXT_SCORE_COLOR = [1,1,0,1]
# color of text for lives
GAME_TEXT_LIVES_COLOR = [1,1,0,1]

# score earned for destroying alien_0
SCORE_ALIEN_0 = 10
# score earned for destroying alien_1
SCORE_ALIEN_1 = 20
# score earned for destroying alien_2
SCORE_ALIEN_2 = 40

# map for aliens' positions
ALIEN_TYPE_MAP = ((0,-1), (0,1), (0,1,2), (0,0,1,2), (0,0,1,1,2), (0,0,0,1,1,2),
                  (0,0,0,1,1,1,2), (0,0,0,1,1,1,2,2), (0,0,0,0,1,1,1,2,2),
                  (0,0,0,0,1,1,1,1,2,2))

# wave state initial
WAVE_STATE_INIT = 0
# wave state clear when ship breaks
WAVE_STATE_SHIP_BREAKING = 1
# wave state clear when all aliens are destroyed
WAVE_STATE_CLEAR = 2
# wave state game over
WAVE_STATE_GAMEOVER = 3


### USE COMMAND LINE ARGUMENTS TO CHANGE NUMBER OF ALIENS IN A ROW"""
"""
sys.argv is a list of the command line arguments when you run Python. These
arguments are everything after the word python. So if you start the game typing

    python invaders 3 4 0.5

Python puts ['breakout.py', '3', '4', '0.5'] into sys.argv. Below, we take
advantage of this fact to change the constants ALIEN_ROWS, ALIENS_IN_ROW, and
ALIEN_SPEED.
"""
try:
    rows = int(sys.argv[1])
    if rows >= 1 and rows <= ALIEN_ROWS_MAX:
        ALIEN_ROWS = rows
except:
    pass # Use original value

try:
    perrow = int(sys.argv[2])
    if perrow >= 1 and perrow <= ALIENS_IN_ROW_MAX:
        ALIENS_IN_ROW = perrow
except:
    pass # Use original value

try:
    speed = float(sys.argv[3])
    if speed > 0 and speed <= 3:
        ALIEN_SPEED = speed
except:
    pass # Use original value

### ADD MORE CONSTANTS (PROPERLY COMMENTED) AS NECESSARY ###
