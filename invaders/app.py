"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders
application. There is no need for any additional classes in this module.
If you need more classes, 99% of the time they belong in either the wave module
or the models module. If you are unsure about where a new class should go,
post a question on Piazza.

YuBin (Kayla) Heo, yh356
December 4th, 2018
"""
from consts import *
from game2d import *
from wave import *
 

# PRIMARY RULE: Invaders can only access attributes in wave.py via get/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an attribute called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from
                consts.py [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
                STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships
                and aliens [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification
    for the method update.

    You may have more attributes if you wish (you might want an attribute to
    store any score across multiple waves). If you add new attributes,
    they need to be documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE
        and create a message (in attribute _text) saying that the user should
        press to play a game.
        """
        # <Extension: Intro Animation>
        self._state = STATE_INTRO
        self._wave = None

        # <Extension: Multiple Waves>
        self._level = 1
        self._backup_score = 0
        self._text = GLabel(text=GAME_TEXT_LEVEL + str(self._level),
                    linecolor=GAME_TEXT_COLOR,
                    font_size=72, font_name='Arcade.ttf',
                    width=GAME_WIDTH, height=GAME_HEIGHT,
                    left=0, bottom=0,
                    halign='center', valign='middle',
                    fillcolor=GAME_TEXT_FILL_COLOR)

        # STATE_COMPLETE Additional Message
        self._text_continue = GLabel(text=GAME_TEXT_CONTINUE,
                    linecolor=GAME_TEXT_CONTINUE_COLOR,
                    font_size=32, font_name='Arcade.ttf',
                    width=GAME_WIDTH, height=50,
                    left=0, bottom=50,
                    halign='center', valign='middle')

        self.lastkeys = 0

        #<Extension: Defense Barriers>
        self.lastkeys_spacebar = 0

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave.
        The primary purpose of this game is to determine the current state,
        and -- if the game is active -- pass the input to the Wave object _wave
        to play the game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.
        It displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the
        screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay. The player can move
        the ship and fire laser bolts.  All of this should be handled inside of
        class Wave (NOT in this class).  Hence the Wave class should have an
        update() method, just like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert type(dt) in [int,float]

        self._determineState()

        #<Extension: Intro Animation>
        if self._state == STATE_INTRO:
            self._updateStateIntro()

        elif self._state == STATE_INACTIVE:
            #<Extension: Multiple Waves>
            self._text.text = GAME_TEXT_LEVEL + str(self._level)

        elif self._state == STATE_NEWWAVE:
            self._wave = Wave()
            #<Extension: Multiple Waves>
            self._wave.score = self._backup_score
            self._backup_score = 0
            self._wave.newwave(self._level)
            #<Extension: Multiple Waves>
            self._state = STATE_ACTIVE

        elif self._state == STATE_ACTIVE:
            self._updateStateActive(dt)

        elif self._state == STATE_PAUSED:
            self._text.text = GAME_TEXT_CONTINUE

        elif self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE

        elif self._state == STATE_COMPLETE:
            self._updateStateComplete()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. To draw
        a GObject g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter. See the example subcontroller.py
        from class.
        """
        #<Extension: Intro Animation>
        if self._state == STATE_INTRO:
            self._introAnimation()
        elif self._state == STATE_PAUSED:
            self._text.draw(self.view)
        elif self._state == STATE_INACTIVE or self._state == STATE_COMPLETE:
            self._text.draw(self.view)
            self._text_continue.draw(self.view)
        else:
             if self._wave != None:
                 self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE

    #<Extension: Intro Animation>
    def _determineState(self):
        """
        Determines the current state and assigns it to self.state

        This method checks for a key press, and if there is one, changes the
        state to the next value.  A key press is when a key is pressed for the
        FIRST TIME. We do not want the state to continue to change as we hold
        down the key.  The user must release the key and press it again to
        change the state.

        parameter: None
        precondition: None
        return: None
        """
        # Determine the current number of keys pressed
        curr_keys = self._input.key_count

        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys == 0

        if change:
            if self._input.is_key_down('c'):
                #<Extension: Intro Animation>
                if self._state == STATE_INTRO:
                    self._state = STATE_INACTIVE
                elif self._state == STATE_INACTIVE:
                    self._state = STATE_NEWWAVE
                elif self._state == STATE_ACTIVE:
                    self._state = STATE_PAUSED
                elif self._state == STATE_PAUSED:
                    self._state = STATE_CONTINUE
                elif self._state == STATE_COMPLETE:
                    if self._level > 1:
                        self._state = STATE_INACTIVE
                    else:
                        self._state = STATE_INTRO

            # # State changed; reset factor
            # self.factor = 0

        # Update last_keys
        self.lastkeys= curr_keys

    def _updateStateIntro(self):
        """
        Helper function for updating STATE_INTRO

        parameter: None
        precondition: None
        return: None
        """
        self._text.text = "Welcome!"
        self._text_continue = GLabel(text=GAME_TEXT_CONTINUE,
                    linecolor=GAME_TEXT_CONTINUE_COLOR,
                    font_size=32, font_name='Arcade.ttf',
                    width=GAME_WIDTH, height=50,
                    left=0, bottom=50,
                    halign='center', valign='middle')

    def _updateStateActive(self,dt):
        """
        Helper function for updating STATE_ACTIVE

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        return : None
        """
        assert type(dt) in [int,float]

        if self._wave != None:
            self._wave.time = self._wave.time + dt
            self._playerKey()
            self._wave.update()
            if self._wave.gamestate == WAVE_STATE_SHIP_BREAKING:
                self._state = STATE_PAUSED
                self._wave.gamestate = WAVE_STATE_INIT
            if self._wave.gamestate == WAVE_STATE_CLEAR:
                self._state = STATE_COMPLETE
            if self._wave.gamestate == WAVE_STATE_GAMEOVER:
                self._state = STATE_COMPLETE

    def _updateStateComplete(self):
        """
        Helper function for updating STATE_COMPLETE

        parameter: None
        precondition: None
        return: None
        """
        if self._wave != None:
            if self._wave.gamestate == WAVE_STATE_CLEAR:
                self._text.text = GAME_TEXT_GAMECLEAR
                #<Extension: Multiple Waves>
                self._backup_score = self._wave.score
                self._level += 1
            elif self._wave.gamestate == WAVE_STATE_GAMEOVER:
                self._text.text = GAME_TEXT_GAMEOVER
                self._level = 1
                self._backup_score = 0
            del self._wave
            self._wave = None

    def _introAnimation(self):
        """
        Helper function for drawing intro animation

        parameter: None
        precondition: None
        return: None
        """
        self._text.draw(self.view)
        self._text_continue.draw(self.view)

    #<Extension: Defense Barriers>
    def _playerKey(self):
        """
        Move the ship and fire bolt by pressing keyboards

        parameter: None
        precondition: None
        return: None
        """
        assert self._wave != None

        if self.input.is_key_down('right'):
            self._wave.moveShip(True)
        if self.input.is_key_down('left'):
            self._wave.moveShip(False)

        self._playerKeyFire()

    def _playerKeyFire(self):
        """
        Specific to firing bolt by pressing keyboards
        Eliminate the firing key pressed down multiple times

        parameter: None
        precondition: None
        return: None
        """
        # Determine the current number of keys pressed
        curr_keys = self._input.key_count

        # Only change if we have just pressed the keys this animation frame
        change = curr_keys > 0 and self.lastkeys_spacebar == 0

        if change:
            if self.input.is_key_down('spacebar'):
                self._wave.firePlayerBolt()

        # Update last_keys
        self.lastkeys_spacebar= curr_keys
