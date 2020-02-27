"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the
Alien Invaders game.  Instances of Wave represent a single wave. Whenever you
move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue. If you do not know, ask on Piazza and we will answer.

YuBin (Kayla) Heo, yh356
December 4th, 2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via get/setters
# Wave is NOT allowed to access anything in app.py
# (Subcontrollers are not permitted to access anything in their parent.


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you should create a NEW instance of Wave
    (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update. See subcontrollers.py from Lecture 24 for an example.
    This class will be similar to than one in how it interacts with the main
    class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave
                 [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen
                 [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Invaders. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Invaders. Only add the
    getters and setters that you need for Invaders. You can keep everything
    else hidden.

    You may change any of the attributes above as you see fit. For example,
    may want to keep track of the score. You also might want some label objects
    to display the score and number of lives. If you make changes, please list
    the changes with the invariants.

    INSTANCE ATTRIBUTES:
        _boltstep: The time between two bolts fired by alien [int or float]
        _score: The amount of score the player earned by destroying aliens
        [int >= 0]
        _walk_dir: The direction of aliens [True is right, False is left]
        _gamestate: The state of game [state constant]
        _breaking_alien_count: The number of aliens destroyed [int]
        _alien_speed: The speed of alien [float]
        _penalty_speed: The penalty speed proportional to the number of
                        alien destroyed [float]
        _text_score: GLabel for displaying the text "score" [GLabel]
        _text_score_num: GLabel for displaying score [GLabel]
        _text_lives: GLabel for displaying the text "lives" [GLabel]
        _text_lives_num: GLabel for displaying live [GLabel]
        _fireboltSound: Sound for fireing bolt [Sound]
        _breakingAlienSound: Sound for Alien destroying [Sound]
        _breakingShipSound: Sound for Ship destroying [Sound]
        _defense_barriers: Values for defense barriers [Sound]
    """

    def __init__(self):
        self._ship = None
        self._aliens = []   # 2D list
        self._bolts = []    # 1D list
        self._dline = None
        self._lives = SHIP_LIVES # number of ships
        self._time = 0

        self._boltstep = 0

        self._score = 0
        self._walk_dir = True
        self._gamestate = WAVE_STATE_INIT

        #<Extension: Speed Up the Aliens>
        self._breakin_alien_count = 0
        self._alien_speed = ALIEN_SPEED

        #<Extension: Multiple Waves>
        self._penalty_speed = 0.0

        self._initText()

        #<Extension: Sound Effects>
        self._fireboltSound = Sound('pew1.wav')
        self._breakingAlienSound = Sound('pew1.wav')
        self._breakingShipSound = Sound('pew2.wav')

        #<Extension: Defense Barriers>
        self._defense_barriers = []

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    #<Extension: Multiple Waves>
    def score(self):
        """
        Score for destroying aliens
        """
        return self._score

    @score.setter
    def score(self,value):
        """
        Setter for score

        Parameter value: Game score
        Precondition value: type of value is int, vlaue >= 0
        Return: None
        """
        assert type(value) == int and value >= 0
        self._score = value

    @property
    def time(self):
        """
        Time for updating animation frame
        """
        return self._time

    @time.setter
    def time(self,value):
        """
        Setter for time

        Parameter value: Time in seconds
        Precondition value: type of value is int or float, value >= 0
        Return: None
        """
        assert type(value) in [int,float]
        self._time = value

    @property
    def gamestate(self):
        """
        States of wave: initial, clear, game over
        """
        return self._gamestate

    @gamestate.setter
    def gamestate(self,value):
        """
        Setter of gamestate

        Parameter value: State of wave
        Precondition value: type of value is int,
                    value >= WAVE_STATE_INIT and value <= WAVE_STATE_GAMEOVER
        Return: None
        """
        assert type(value) == int
        assert value >= WAVE_STATE_INIT and value <= WAVE_STATE_GAMEOVER
        self._gamestate = value

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    #<Extension: Multiple Waves>
    def newwave(self,level):
        """
        States of wave: initial, clear, game over

        Parameter level: Game level
        Precondition level: type of value is int, value >= 1
        Return: None
        """
        assert(ALIEN_ROWS >= 1 and ALIEN_ROWS <= ALIEN_ROWS_MAX)
        assert(ALIENS_IN_ROW >= 1 and ALIENS_IN_ROW <= ALIENS_IN_ROW_MAX)
        assert(len(ALIEN_TYPE_MAP) == ALIEN_ROWS_MAX)
        assert(type(level) == int and level >= 1)

        self._defined = False
        self._walk_dir = True
        self._boltstep = random.randrange(1, BOLT_RATE+1)
        self._newgamestate()
        # create DEFENSE LINE
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linewidth=1,linecolor=DEFENSE_LINE_COLOR)
        # create ship
        self._newship()
        #<Extension: Speed Up the Aliens>
        self._breakin_alien_count = 0
        self._alien_speed = ALIEN_SPEED
        #<Extension: Multiple Waves>
        self._newpenaltyspeed(level)

        #<Extension: Animate the Aliens>
        self._defined = True

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self):
        """
        Animates a single frame in the game.

        Parameter: None
        Precondition: None
        Return: None
        """

        if self._time >= self._alien_speed:
            #<Extension: Speed Up the Aliens>.
            walk_horz = 0
            if self._is_horizontal_end():
                self._change_walk_dir()
            else:
                walk_horz = ALIEN_H_WALK
                if self._walk_dir == False:
                    walk_horz = -ALIEN_H_WALK
            if walk_horz != 0:
                if self._collision_defense_line():
                    self._gamestate = WAVE_STATE_GAMEOVER
            self._moveAliens(walk_horz)
            self._fireAlienBolt()
            self._time = 0

        if len(self._bolts) > 0:
            self._moveBolts()
            self._collisionBolts()
        #<Extension: Defense Barriers>
        self._collisionDefenseBarriers()
        self._breakinAnimation()
        self._text_score_num.text = str(self._score)
        self._text_lives_num.text = str(self._lives)


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view.

        Parameter: None
        Precondition: None
        Return: None
        """

        self._text_score.draw(view)
        self._text_score_num.draw(view)
        self._text_lives.draw(view)
        self._text_lives_num.draw(view)

        self._dline.draw(view)

        for aliens in self._aliens:
            for alien in aliens:
                if alien != None:
                    alien.draw(view)

        if self._ship:
            self._ship.draw(view)

        for bolt in self._bolts:
            bolt.draw(view)

        #<Extension: Defense Barriers>
        for i in range(DEFENSE_BARRIERS_NUM):
            if self._defense_barriers[i] != None:
                self._defense_barriers[i].draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    #<Extension: Defense Barriers>
    def _initText(self):
        """
        Helper function for initializing texts

        Parameter: None
        Precondition: None
        Return: None
        """
        self._text_score = GLabel(text=GAME_TEXT_SCORE,
                    linecolor=GAME_TEXT_SCORE_COLOR,
                    font_size=48, font_name='Arcade.ttf',
                    left=ALIEN_H_SEP, bottom=GAME_HEIGHT-60)
        self._text_score_num = GLabel(text="0", linecolor=GAME_TEXT_COLOR,
                    font_size=48, font_name='Arcade.ttf',
                    left=ALIEN_H_SEP + 140, bottom=GAME_HEIGHT-60)
        self._text_lives = GLabel(text=GAME_TEXT_LIVES,
                    linecolor=GAME_TEXT_LIVES_COLOR,
                    font_size=48, font_name='Arcade.ttf',
                    left=GAME_WIDTH - 170, bottom=GAME_HEIGHT-60)
        self._text_lives_num = GLabel(text="0", linecolor=GAME_TEXT_COLOR,
                    font_size=48, font_name='Arcade.ttf',
                    left=GAME_WIDTH - 40, bottom=GAME_HEIGHT-60)

    def _newgamestate(self):
        """
        Helper function for gamestate in method newwave

        Parameter: None
        Precondition: None
        Return: None
        """
        self._gamestate = WAVE_STATE_INIT

        sz = (ALIEN_HEIGHT + ALIEN_V_SEP) * (ALIEN_ROWS - 1)
        sy = (GAME_HEIGHT - ALIEN_CEILING) - sz
        for i in range(ALIEN_ROWS):
            self._aliens.append([])
            sx = ALIEN_H_SEP
            alientype = int(ALIEN_TYPE_MAP[ALIEN_ROWS-1][i])
            for j in range(ALIENS_IN_ROW):

    #<Extension: Animate the Aliens>
                alien = Alien(x=sx + ALIEN_WIDTH/2,y=sy + ALIEN_HEIGHT/2,
                              width=ALIEN_WIDTH,height=ALIEN_HEIGHT,
                              source=ALIEN_IMAGES[alientype],
                              format=(3,2))
                self._aliens[i].append(alien)
                sx = sx + (ALIEN_WIDTH + ALIEN_H_SEP)
            sy = sy + (ALIEN_HEIGHT + ALIEN_V_SEP)

    def _newship(self):
        """
        Helper function for creating ship in method newwave

        Parameter: None
        Precondition: None
        Return: None
        """
        self._ship = Ship(x=(GAME_WIDTH - SHIP_WIDTH)/2,
                          y=SHIP_BOTTOM + SHIP_HEIGHT/2,
                          width=SHIP_WIDTH,height=SHIP_HEIGHT,
                          source=SHIP_IMAGE,
                          format=(2,3))

    def _newpenaltyspeed(self,level):
        """
        Helper function for penalty speed of alien in method newwave

        Parameter level: Game level
        precondition level: type of value is int, value >= 1
        Return: None
        """
        assert(type(level) == int and level >= 1)

        penalty = ((ALIEN_SPEED * 0.1) * min(level-1, 9))
        self._penalty_speed = 0.0 if level == 1 else penalty

        #<Extension: Defense Barriers>
        sx = DEFENSE_BARRIERS_SEP
        for i in range(DEFENSE_BARRIERS_NUM):
            defensebarriers = DefenseBarriers(x=sx + DEFENSE_BARRIERS_WIDTH/2,
                          y=DEFENSE_BARRIERS_LINE,
                          width=DEFENSE_BARRIERS_WIDTH,
                          height=DEFENSE_BARRIERS_HEIGHT,
                          source='defense-strip.png',
                          format=(5,2))
            self._defense_barriers.append(defensebarriers)
            sx += DEFENSE_BARRIERS_WIDTH + DEFENSE_BARRIERS_SEP

    def _collisionDefenseBarriers(self):
        """
        Check for collision between bolt and barrier
        DefenseBarriers weeken if collide with bolt

        Parameter: None
        Precondition: None
        Return: None
        """
        if self._breakin_alien_count < ALIEN_ROWS * ALIENS_IN_ROW:
            for d in range(DEFENSE_BARRIERS_NUM):
                defense = self._defense_barriers[d]
                if defense != None:
                    if self._defenseBarriers_collision_alien(defense):
                        if defense.frame < DEFENSE_BARRIERS_FRAMES:
                            defense.frame += 1
                        else:
                            del defense
                            self._defense_barriers[d] = None

        if len(self._bolts) > 0:
            for d in range(DEFENSE_BARRIERS_NUM):
                defense = self._defense_barriers[d]
                if defense != None:
                    i = 0
                    while i < len(self._bolts):
                        if defense.collides(self._bolts[i]):
                            del self._bolts[i]
                            if defense.frame < DEFENSE_BARRIERS_FRAMES:
                                defense.frame += 1
                            else:
                                del defense
                                self._defense_barriers[d] = None
                            break
                        else:
                            i += 1

    def _defenseBarriers_collision_alien(self, defense):
        """
        Check collision between alien and defense barriers

        Parameter defense: defense is barrier object
        Precondition defense: defense is not None, type is DefenseBarriers
        Return: 'True' if alien and defense collides, 'False' if not
        """
        assert defense != None and type(defense) == DefenseBarriers

        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                alien = self._aliens[i][j]
                if alien != None and alien.live and defense.collides(alien):
                    alien.live = False
                    alientype = int(ALIEN_TYPE_MAP[ALIEN_ROWS-1][i])
                    self._score += ALIEN_SCORE[alientype]
                    self._breakin_alien_count += 1
                    return True
        return False

    #<Extension: Animate the Aliens>
    def _breakinAnimation(self):
        """
        Manage alien's animation frame and destroyed ship

        Parameter: None
        Precondition: None
        Return: None
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                alien = self._aliens[i][j]
                if alien != None and alien.live == False:
                    if alien.frame < 5:
                        alien.frame += 1
                    else:
                        del alien
                        self._aliens[i][j] = None
        if self._ship:
            if self._ship.live == False:
                if self._ship.frame < 5:
                    self._ship.frame += 1
                else:
                    self._breakingShip()

    def _moveAliens(self, walk_horz):
        """
        Move the position of aliens

        Parameter walk_horz: alien's horizontal, vertical movement
        Precondition walk_horz: type is int or float,
                0 is vertical down; if not 0, amount of horizontal movement
        Return: None
        """
        assert type(walk_horz) in [int,float]
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                alien = self._aliens[i][j]
                if alien != None:
                    if walk_horz != 0:
                        alien.x = alien.x + walk_horz
                    else:
                        alien.y = alien.y - ALIEN_V_WALK
                    if alien.live:
                        alien.frame = (alien.frame+1) % 2

    def _moveBolts(self):
        """
        Move the position of bolts

        Parameter: None
        Precondition: None
        Return: None
        """
        for bolt in self._bolts:
            bolt.y = bolt.y + bolt.velocity
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].isPlayerBolt():
                if (self._bolts[i].y - BOLT_HEIGHT/2) > GAME_HEIGHT:
                    del self._bolts[i]
                else:
                    i += 1
            else:
                if (self._bolts[i].y + BOLT_HEIGHT/2) <= 0:
                    del self._bolts[i]
                else:
                    i += 1

    def _breakingShip(self):
        """
        Destroying ships

        Parameter: None
        Precondition: None
        Return: None
        """
        assert self._lives > 0
        assert self._ship != None

        self._lives -= 1

    #<Extension: Animate the Aliens>
        self._ship.live = True
        if self._lives > 0:
            self._gamestate = WAVE_STATE_SHIP_BREAKING
        else:
            self._gamestate = WAVE_STATE_GAMEOVER
        self._bolts.clear()

    def _checkClearAlien(self):
        """
        Keep in track of the number and speed of aliens

        Parameter: None
        Precondition: None
        Return: None
        """
        #<Extension: Multiple Waves>
        assert(ALIEN_SPEED > self._penalty_speed)
        if self._breakin_alien_count > 0:
            ar = (self._breakin_alien_count + 1) / (ALIEN_ROWS * ALIENS_IN_ROW)
            bac = (1.0 - ar * ALIEN_SPEED_RATIO)
            self._alien_speed = (ALIEN_SPEED - self._penalty_speed) * bac
        if self._breakin_alien_count == ALIEN_ROWS * ALIENS_IN_ROW:
            self._gamestate = WAVE_STATE_CLEAR
            self._bolts.clear()

    def _collisionBolts(self):
        """
        Check for collision between bolts
        Player bolt checks collision with alien
        Alien bolt checks collision with ship

        Parameter: None
        Precondition: None
        Return: None
        """

        i = 0
        while i < len(self._bolts):
            if self._bolts[i].isPlayerBolt():
                if self._bolt_collision_alien(self._bolts[i]):
                    del self._bolts[i]
                    self._checkClearAlien()
        #<Extension: Sound Effects>
                    self._breakingAlienSound.play()
                    return
                else:
                    i += 1
            else:
                if self._bolt_collision_ship(self._bolts[i]):
                    del self._bolts[i]
        #<Extension: Animate the Aliens>
                    self._ship.live = False

        #<Extension: Sound Effects>
                    self._breakingShipSound.play()
                    return
                else:
                    i += 1

    def _bolt_collision_alien(self, bolt):
        """
        Check for collision between player's bolt and alien

        Parameter bolt: Bolt object
        Precondition bolt: bolt is not None, type is Bolt,
            bolt is bolt fired by ship
        Return: 'True' if bolt and aline collide, 'False' if not
        """
        assert bolt != None and type(bolt) == Bolt and bolt.isPlayerBolt()

        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                alien = self._aliens[i][j]
                if alien != None and alien.collides(bolt):
                    alien.live = False
                    alientype = int(ALIEN_TYPE_MAP[ALIEN_ROWS-1][i])
                    self._score += ALIEN_SCORE[alientype]
                    self._breakin_alien_count += 1
                    return True
        return False

    def _bolt_collision_ship(self, bolt):
        """
        Check for collision between alien bolt and ship

        Parameter bolt: Bolt object
        Precondition bolt: bolt is not None, type is Bolt,
            bolt is bolt fired by alien
        Return: 'True' if bolt and aline collide, 'False' if not
        """
        assert bolt != None and not bolt.isPlayerBolt()

        if self._ship != None and self._ship.collides(bolt):
            return True
        return False

    def _collision_defense_line(self):
        """
        Check if alien crossed the defense_line
        _is_horizontal_end() meets the condition

        Parameter: None
        Precondition: None
        Return: None
        """
        for i in range(ALIEN_ROWS):
            for j in range(ALIENS_IN_ROW):
                alien = self._aliens[i][j]
                if alien != None:
                    if (alien.y - ALIEN_HEIGHT/2) <= DEFENSE_LINE:
                        return True
                    break;
        return False

    def _existPlayerBolt(self):
        """
        Players stop shooting bolt

        Parameter: None
        Precondition: None
        Return: None
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return True
        return False

    def firePlayerBolt(self):
        """
        Players shot bolt

        Parameter: None
        Precondition: None
        Return: None
        """
        assert self._ship != None
        if not self._existPlayerBolt():
            bolt = Bolt(True, x=self._ship.x, y=self._ship.y+SHIP_HEIGHT/2)

            self._bolts.append(bolt)
    #<Extension: Sound Effect>
            self._fireboltSound.play()

    def _selectFireBoltAlien(self):
        """
        Chooses the alien that creates bolt randomly
        One of the aliens at the bottom line

        Parameter: None
        Precondition: None
        Return: None
        """
        aliens = []
        for j in range(ALIENS_IN_ROW):
            for i in range(ALIEN_ROWS):
                if self._aliens[i][j] != None:
                    aliens.append(self._aliens[i][j])
                    break

        if len(aliens) == 0:
            return None
        return random.choice(aliens)

    def _fireAlienBolt(self):
        """
        Create Bolt from alien when  _boltstep is 0
        Alien to shoot the bolt is chosen by _selectFireBoltAlien()
        if _boltstep is 0, it randomly chooses a new step number (1 ~ BOLT_RATE)

        Parameter: None
        Precondition: None
        Return: None
        """
        assert self._boltstep > 0
        self._boltstep -= 1
        if self._boltstep == 0:
            alien = self._selectFireBoltAlien()
            if alien != None:
                bolt = Bolt(False, x=alien.x, y=alien.y-ALIEN_HEIGHT/2)
                self._bolts.append(bolt)
            self._boltstep = random.randrange(1,BOLT_RATE+1)

    def moveShip(self, right):
        """
        Move the ship

        Parameter right: movement of right and left
        Precondition right: Type is bool,
            True if ship moves right, False if ship moves left
        Return: None
        """

        assert type(right) == bool
        assert self._ship != None
        x = self._ship.x + (SHIP_MOVEMENT if right else -SHIP_MOVEMENT)
        self._ship.x = min(max(x, SHIP_WIDTH/2), GAME_WIDTH - SHIP_WIDTH/2)

    def _is_horizontal_end(self):
        """
        Check whether alien is at the sides of game screen
        _walk_dir is True when it checks the right side
        _walk_dir is False when it checks the left side

        Parameter: None
        Precondition: None
        Return: None
        """
        horizontal_end = False

        if self._walk_dir:
            for i in range(ALIEN_ROWS):
                for j in range(ALIENS_IN_ROW):
                    alien = self._aliens[i][ALIENS_IN_ROW - 1 - j]
                    if alien != None:
                        ad = (GAME_WIDTH - ALIEN_WIDTH/2 - ALIEN_H_SEP)
                        if (alien.x + ALIEN_H_WALK) > ad:
                            horizontal_end = True
                        break;
                if horizontal_end == True:
                    break
        else:
            for i in range(ALIEN_ROWS):
                for j in range(ALIENS_IN_ROW):
                    alien = self._aliens[i][j]
                    if alien != None:
                        ah = (ALIEN_WIDTH/2 + ALIEN_H_SEP)
                        if (alien.x - ALIEN_H_WALK) < ah:
                            horizontal_end = True
                        break;
                if horizontal_end == True:
                    break
        return horizontal_end

    def _change_walk_dir(self):
        """
        Change the direction of alien

        Parameter: None
        Precondition: None
        Return: None
        """
        self._walk_dir = not self._walk_dir
