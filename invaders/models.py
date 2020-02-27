"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game.
Anything that you interact with on the screen is model: the ship,
the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class
for it. Unless you need something special for your extra gameplay features,
Ship and Aliens could just be an instance of GImage that you move across the
screen. You only need a new class when you add extra features to an object.
So technically Bolt, which has a velocity, is really the only model that needs
to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the objects,
and you might want to add a custom initializer. With that said, feel free to
keep the pass underneath the class definitions if you do not want to do that.

You are free to add even more models to this module. You may wish to do this
when you add new features to your game, such as power-ups. If you are unsure
about whether to make a new class or not, please ask on Piazza.

YuBin (Kayla) Heo, yh356
December 4th, 2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py. If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as an argument when it
# calls the method.

#<Extension: Animate the Aliens ...>
class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship. While moving a ship
    just means changing the x attribute (which you can do directly), you want
    to prevent the player from moving the ship offscreen. This is an ideal
    thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do
    not require this. You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide with
    different bolts. Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to keep
    this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them for
    extra gameplay features (like animation). If you add attributes,
    list them below.

    INSTANCE ATTRIBUTES:
        _live: live of the ship [bool]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """
        Initializer for class Ship

        You do not need to provide the keywords as a dictionary.
        The ** in the parameter `keywords` does that automatically.

        Any attribute of this class may be used as a keyword. The argument must
        satisfy the invariants of that attribute. See the list of attributes
        of this class for more information.

        Parameter **keywords: dictionary of keyword arguments
        Type **keywords:  keys are attribute names
        """
        #<Extension: Animate the Aliens>
        GSprite.__init__(self,**keywords)
        self._live = True

    @property
    def live(self):
        """
        Determine whether ship is destroyed or not for GSprite frame

        Return: Whether the ship is alive or not
        """
        return self._live

    @live.setter
    def live(self,value):
        """
        Setter for live

        If live is true, set frame to 0
        If live is false, set frame to 1

        Parameter value: whether alien is alive or not
        Precondition value: Type is boolean
        Return: none
        """
        assert type(value) == bool
        self._live = value
        self.frame = 0 if value else 1

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Check if the ship and bolt collides

        Parameter bolt: Bolt object
        Precondition bolt: bolt is not None, type is Bolt
        Return: 'True' if ship and bolt collide, 'False' if it did not collide
        """
        assert bolt != None and type(bolt) == Bolt

        sx1 = self.x - self.width/2
        sy1 = self.y - self.height/2
        sx2 = self.x + self.width/2
        sy2 = self.y + self.height/2

        bx1 = bolt.x - bolt.width/2
        by1 = bolt.y - bolt.height/2
        bx2 = bolt.x + bolt.width/2
        by2 = bolt.y + bolt.height/2

        return (sx2 >= bx1 and sx1 <= bx2) and (sy2 >= by1 and sy1 <= by2)


#<Extension : Animate the Aliens>
class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do
    not require this. You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide with
    different bolts. Ships collide with Alien bolts, not Ship bolts. And Aliens
    collide with Ship bolts, not Alien bolts. An easy way to keep this straight
    is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them for
    extra gameplay features (like giving each alien a score value).
    If you add attributes, list them below.

    INSTANCE ATTRIBUTES:
        _live: live of the aliens [bool]
    """
    # INITIALIZER TO CREATE AN ALIEN
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """
        Initializer for class Alien

        You do not need to provide the keywords as a dictionary.
        The ** in the parameter
        `keywords` does that automatically.

        Any attribute of this class may be used as a keyword. The argument must
        satisfy the invariants of that attribute. See the list of attributes
        of this class for more information.

        Parameter keywords: dictionary of keyword arguments
        Type keywords: keys are attribute names
        """
        GSprite.__init__(self,**keywords)
        self._live = True

    @property
    def live(self):
        """
        Determine whether alien is destroyed or not for GSprite frame

        Return: whether alien is alive or not
        """
        return self._live

    @live.setter
    def live(self,value):
        """
        Setter for live

        if live is true, set frame to 0
        if live is false, set frame to 2

        Parameter vlaue: Whether alien is alive or not
        Precondition value: Type is bool
        Return: None
        """
        assert type(value) == bool
        self._live = value
        self.frame = 0 if value else 2

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Check if the alien and bolt collides

        Parameter bolt: Bolt object
        Precondition bolt: bolt is not None, type is Bolt
        Return: 'True' if alien and bolt collide, 'False' if it did not collide
        """
        assert bolt != None and type(bolt) == Bolt

        sx1 = self.x - self.width/2
        sy1 = self.y - self.height/2
        sx2 = self.x + self.width/2
        sy2 = self.y + self.height/2

        bx1 = bolt.x - bolt.width/2
        by1 = bolt.y - bolt.height/2
        bx2 = bolt.x + bolt.width/2
        by2 = bolt.y + bolt.height/2

        return (sx2 >= bx1 and sx1 <= bx2) and (sy2 >= by1 and sy1 <= by2)


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because
    we need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a helper.

    You also MIGHT want to create a method to move the bolt. You move the bolt
    by adding the velocity to the y-position.  However, the getter allows Wave
    to do this on its own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    """

    def __init__ (self,up,**keywords):
        """
        Initializer for class Bolt

        You do not need to provide the keywords as a dictionary.
        The ** in the parameter `keywords` does that automatically.

        Any attribute of this class may be used as a keyword. The argument
        must satisfy the invariants of that attribute. See the list of
        attributes of this class for more information.

        Parameter keywords: dictionary of keyword arguments
        Type keywords: keys are attribute names
        """
        assert type(up) == bool
        GRectangle.__init__(self,**keywords,width=BOLT_WIDTH,height=BOLT_HEIGHT,
        fillcolor=BOLT_COLOR)
        self._velocity = BOLT_SPEED if up else -BOLT_SPEED

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    def velocity(self):
        """
        Velocity of bolt, negative value for alien and positive value for ship
        """
        return self._velocity

    @velocity.setter
    def velocity(self,value):
        """
        Setter for velocity

        Parameter value: Velocity of Bolt
        Precondition bolt: value is int or float type, positive if bolt is
            fired by ship, negative if bolt is fired by alien
        Return: None
        """
        assert type(value) in [int,float]
        assert value != 0
        self._velocity = value

    # INITIALIZER TO SET THE VELOCITY

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Distinguish bolts from the ship's shot and the alien.

        Parameter: None
        Precondition: None
        Return: 'True' if ship fires bolt, 'False' is alien fires bolt
        """
        return self._velocity > 0


#<=확장 : Defense Barriers ...>
class DefenseBarriers(GSprite):
    """
    Barrier to protect the ship
    DefenseBarriers weeken when they collide with either bolt or alien.
    Strength is managed by DEFENSE_BARRIERS_FRAMES (using GSprite frame)
    """
    # INITIALIZER TO CREATE AN DefenseBarriers
    # BUILT-IN METHODS
    def __init__(self,**keywords):
        """
        Initializer for class DefenseBarriers

        You do not need to provide the keywords as a dictionary.
        The ** in the parameter `keywords` does that automatically.

        Any attribute of this class may be used as a keyword. The argument
        must satisfy the invariants of that attribute. See the list of
        attributes of this class for more information.

        Parameter keywords: dictionary of keyword arguments
        Type keywords:  keys are attribute names
        """
        GSprite.__init__(self,**keywords)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,obj):
        """
        Check if the alien and bolt collide with defense barriers

        Parameter obj: Alien or Bolt object
        Precondition obj: obj is not None, type is Alien or Bolt
        Return: 'True' if DefenseBarriers and obj collides, 'False' if not
        """
        assert obj != None and (type(obj) == Alien or type(obj) == Bolt)

        sx1 = self.x - self.width/2
        sy1 = self.y - self.height/2 - DEFENSE_BARRIERS_COLLIDES_GAP
        sx2 = self.x + self.width/2
        sy2 = self.y + self.height/2 - DEFENSE_BARRIERS_COLLIDES_GAP

        bx1 = obj.x - obj.width/2
        by1 = obj.y - obj.height/2
        bx2 = obj.x + obj.width/2
        by2 = obj.y + obj.height/2

        return (sx2 >= bx1 and sx1 <= bx2) and (sy2 >= by1 and sy1 <= by2)
