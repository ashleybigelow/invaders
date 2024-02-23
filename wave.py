"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Ashley Bigelow (arb395)
# 12/12/19
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _counter: the number of laps the aliens have done
    # Invarient: _counter is an int >= 0
    #
    # Attribute _stepsToBolt: the number of steps until an alien shoots
    # Invarient: _stepsToBolt is an int >= 0
    #
    # Attribute _numSteps: the number of steps the aliens have taken
    # Invarient: _numSteps is an int >=0
    #
    # Attribute _lives: the number of lives the player has. This gets passed
    # over from the Invaders class.
    # Invarient: _lives is an int >= 0 and <= 3
    #
    # Attribute _speed: determines how fast the aliens walk across the screen
    # Invarient: _speed is a float <= 1
    #
    # Attribute _score: the score of the player
    # Invarient: _score is an int >= 0
    #
    # Attribute _scorelabel: the label for the score that goes on the screen
    # Invarient: _scorelabel is a GLabel object
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.

    def getShip(self):
        """
        returns the ship that is currently on the screen
        """
        return self._ship

    def setShip(self, newship):
        """
        sets the ship on the screen to the newship

        newship is a ship object
        """
        self._ship = newship

    def getAliens(self):
        """
        return the 2D list of aliens
        """
        return self._aliens

    def getScore(self):
        """
        returns the players score"
        """
        return self._score

    def setScore(self, newscore):
        """
        sets the players score to newscore
        """
        self._score = newscore

    def getScoreLabel(self):
        """
        returns the scorelabel
        """
        return self._scorelabel

    def setScoreLabel(self, newscorelabel):
        """
        sets the score label to newscorelabel
        """
        self._scorelabel = newscorelabel

    def __init__(self, waveNumber, lives, score):
        """
        Initializes each of the elements of the gmae

        Parameter waveNumber: the number of the wave the player is on
        Precondition: waveNumber is an integer >= 0

        Parameter lives: the number of lives the player has
        Precondition: lives is an integer >= 0 or <= 3
        """
        self._time = 0
        self._bolts = []
        self._aliens = self.init_helper()
        self._counter = 0
        self._ship = Ship()
        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
                                            linewidth = 2, linecolor= 'black')
        self._stepsToBolt = random.randint(1, BOLT_RATE)
        self._numSteps = 0
        self._lives = lives
        self._speed = ALIEN_SPEED*(0.75)**(waveNumber-1)
        self._score = score
        self._scorelabel = GLabel(text="Score: "+ str(self._score),\
            font_size=30, font_name = 'Arcade.ttf', x=80, y=GAME_HEIGHT - 80)

    def init_helper(self, row=ALIEN_ROWS, col=ALIENS_IN_ROW):
        """
        Creates a 2D list of aliens

        Parameter row: the number of rows in the list
        Precondition: row is an int > 0

        Parameter col: the number of collumns in the list
        Precondition: col is an int > 0
        """
        answer = []
        for r in range(row):
            rowanswer = []
            yval = GAME_HEIGHT-(ALIEN_CEILING+(r+1/2)*\
                        (ALIEN_HEIGHT)+r*(ALIEN_V_SEP))
            for c in range(col):
                xval = (ALIEN_H_SEP)*(c+1)+(ALIEN_WIDTH)*(c+1/2)
                if r%6==1 or r%6==2:
                    rowanswer.append(Alien(xval, yval, ALIEN_IMAGES[1]))
                elif r%6==3 or r%6==4:
                    rowanswer.append(Alien(xval, yval, ALIEN_IMAGES[2]))
                elif r%6==5 or r%6==0:
                    rowanswer.append(Alien(xval, yval, ALIEN_IMAGES[0]))
            answer.append(rowanswer)
        return answer

    def update(self, input, dt=0):
        """
        Gets called each animation frame to update all of the elements on the
        screen

        Parameter input: used to detect what button a player presses
        Precondition: input is a GInput object

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        #moves the ship
        if input.is_key_down('left') and self._ship != None:
            if self._ship.x >= SHIP_WIDTH/2:
                self._ship.x= self._ship.x - SHIP_MOVEMENT
        if input.is_key_down('right') and self._ship != None:
            if self._ship.x <= GAME_WIDTH-SHIP_WIDTH/2:
                self._ship.x= self._ship.x + SHIP_MOVEMENT
        #keeps track of the time
        self._time = self._time + dt
        #moves the aliens
        self._aliens = Wave.aliensGone(self._aliens)
        if self._time > self._speed and len(self._aliens) != 0 and \
                            not Wave.aliens_below_line(self._aliens):
            if self._counter%4 == 0:
                self._move_alien_right()
            elif self._counter%4 == 1 or self._counter%4 == 3:
                self._move_alien_down()
            else:
                self._move_alien_left()
        #shoots a bolt if up arrow is pressed
        if input.is_key_down('up') and self._ship != None:
            if Wave._numPlayerBolts(self._bolts) == 0:
                newbolt = Bolt(xi = self._ship.x, yi = SHIP_BOTTOM+SHIP_HEIGHT,\
                                    widthi = BOLT_WIDTH, heighti = BOLT_HEIGHT)
                self._bolts.append(newbolt)
        #updates to check for collisions and moves bolts
        if len(self._bolts) > 0:
            self._moveBolt()
            self._checkAlienCollision()
            if Wave._checkShipCollision(ship = self._ship,\
                boltlist = self._bolts, lives= self._lives):
                self._ship = None
                self._lives = self._lives-1
        #causes aliens to shoot bolts
        self.alienShoot()

    def alienShoot(self):
        """
        causes an alien to shoot
        """
        if self._numSteps == self._stepsToBolt:
            newbolt = Wave._randAlien(self._aliens)
            self._bolts.append(newbolt)
            self._numSteps = 0
            self._stepsToBolt = random.randint(1, BOLT_RATE)

    def aliens_below_line(alienlist):
        """
        returns True if the aliens pass the line, otherwise returns False

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        bottomRow = Wave._alien_bottom_row(alienlist)
        alien = Wave._alien_from_row(bottomRow)
        if (alien.y - ALIEN_HEIGHT/2) < DEFENSE_LINE:
            return True
        return False

    #moving the aliens
    def _move_alien_right(self):
        """
        A method that moves all of the aliens to the right
        """
        # rightAlien = Wave.pickRightEdge(self._aliens)
        rightAlien = Wave._alien_from_right_col(self._aliens)
        if rightAlien.x < (GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH):
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    curalien = self._aliens[row][alien]
                    if not curalien == None:
                        curalien.x = curalien.x + ALIEN_H_SEP
                    self._time = 0
            self._numSteps = self._numSteps + 1
        else:
            self._counter = self._counter + 1

    def _move_alien_left(self):
        """
        A method that moves all of the aliens to the left
        """
        # leftAlien = Wave.pickLeftEdge(self._aliens)
        leftAlien = Wave._alien_from_left_col(self._aliens)
        if leftAlien.x > (ALIEN_H_SEP + (ALIEN_WIDTH)):
            for row in range(ALIEN_ROWS):
                for alien in range(ALIENS_IN_ROW):
                    curalien = self._aliens[row][alien]
                    if not curalien == None:
                        curalien.x = curalien.x - ALIEN_H_SEP
                    self._time = 0
            self._numSteps = self._numSteps + 1
        else:
            self._counter = self._counter + 1

    def _move_alien_down(self):
        """
        A method that moves all of the aliens down
        """
        for row in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                curalien = self._aliens[row][alien]
                if not curalien == None:
                    curalien.y = curalien.y - ALIEN_V_SEP
                self._time = 0
        self._numSteps = self._numSteps + 1
        self._counter = self._counter + 1

    def _moveBolt(self):
        """
        Moves all the bolts and deletes them when they go off the screen
        """
        #moves each ship bolt up
        for bolt in range(len(self._bolts)):
            self._bolts[bolt].y = self._bolts[bolt].y + \
                            self._bolts[bolt]._velocity
        #deletes a bolt when it goes off the screen
        i = 0
        while i < len(self._bolts):
            if (self._bolts[i].y - BOLT_HEIGHT/2) > GAME_HEIGHT or\
                            (self._bolts[i].y + BOLT_HEIGHT/2) < 0:
                del self._bolts[i]
            else:
                i += 1

    def draw(self, view):
        """
        Draws a single wave and the ship.

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.

        Parameter view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        for row in range(ALIEN_ROWS):
            for alien in range(ALIENS_IN_ROW):
                if not self._aliens[row][alien] == None:
                    self._aliens[row][alien].draw(view)
        if not self._ship == None:
            self._ship.draw(view)
        self._dline.draw(view)
        for i in range(len(self._bolts)):
            self._bolts[i].draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _isPlayerBolt(objbolt):
        """
        checks a bolt to see if it has come from the ship

        Parameter objbolt: the bolt that is being checked
        Precondition: objbolt is a Bolt object
        """
        if objbolt._velocity > 0:
            return True
        return False

    def _numPlayerBolts(boltlist):
        """
        Returns the number of bolts that exist in the boltlist

        Parameter boltlist: the boltlist that will be checked
        Precondition: boltlist is a list of Bolt objects
        """
        num = 0
        for bolt in range(len(boltlist)):
            if Wave._isPlayerBolt(boltlist[bolt]):
                num = num + 1
        return num

    def _randAlien(alienlist):
        """
        chooses a random alien from the bottom row of alienlist and causes it to
        fire a bullet

        Parameter alienlist: a list of aliens to choose from
        Precondition: alienlist is a 2D list of Alien objects or None is the
        alien has been deleted
        """
        #causes an alien to shoot a bolt
        randomcollumn = random.randint (0, ALIENS_IN_ROW-1)
        while alienlist[0][randomcollumn] == None:
            randomcollumn = random.randint (0, ALIENS_IN_ROW-1)
        randomAlien = alienlist[ALIEN_ROWS-1][randomcollumn]
        x = 2
        while randomAlien == None:
            randomAlien = alienlist[ALIEN_ROWS-x][randomcollumn]
            x = x + 1
        newbolt = Bolt(xi = randomAlien.x, yi = randomAlien.y - ALIEN_HEIGHT,\
                widthi = BOLT_WIDTH, heighti = BOLT_HEIGHT, fillcolori = 'red')
        newbolt._velocity = -BOLT_SPEED
        return newbolt

    def _checkAlienCollision(self):
        """
        takes in an alien list and checks for a collision. If there is one, it
        deletes the alien and bolt involved and returns true to stop the loop

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted

        Parameter boltlist: the list of bolts to check from
        Precondition: boltlist is a list of Bolt objects
        """
        for aBolt in range(len(self._bolts)):
            for row in range(ALIEN_ROWS):
                for col in range(ALIENS_IN_ROW):
                    if not (self._aliens[row][col] == None):
                        if Wave._isPlayerBolt(self._bolts[aBolt]):
                            if self._aliens[row][col].collidesAlien(self._bolts\
                                                                    [aBolt]):
                                del self._bolts[aBolt]
                                if self._aliens[row][col].source == ALIEN_IMAGES[0]:
                                    self._score = self._score + 30
                                    self._scorelabel = GLabel(text="Score: "+\
                                     str(self._score),font_size=30, font_name =\
                                     'Arcade.ttf', x=80, y=GAME_HEIGHT - 80)
                                elif self._aliens[row][col].source == \
                                                        ALIEN_IMAGES[1]:
                                    self._score = self._score +20
                                    self._scorelabel = GLabel(text="Score: "+\
                                     str(self._score),font_size=30, font_name =\
                                      'Arcade.ttf', x=80, y=GAME_HEIGHT - 80)
                                else:
                                    self._score = self._score + 10
                                    self._scorelabel = GLabel(text="Score: "+\
                                     str(self._score),font_size=30, font_name =\
                                      'Arcade.ttf', x=80, y=GAME_HEIGHT - 80)
                                self._aliens[row][col] = None
                                return True

    def _checkShipCollision(ship, boltlist, lives):
        """
        returns True when a bolt collides with the ship

        Parameter ship: the players ship
        Precondition: ship is a Ship() object

        Parameter boltlist: the list of bolts to check
        Precondition: boltlist is a list of Bolt objects

        Parameter lives: the number of lives the player has left
        Precondition: lives is an int >= 0 and <= 3
        """
        for aBolt in range(len(boltlist)):
            if ship != None:
                if ship.collidesShip(boltlist[aBolt]):
                    del boltlist[aBolt]
                    if lives > 0:
                        lives = lives - 1
                    return True

    def _lowest_aliens(alienlist):
        """
        returns a 1D list of the lowest aliens in each non-empty collumn

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        answer = []
        for col in range(ALIENS_IN_ROW):
            i = col + 1
            for row in range(ALIEN_ROWS):
                if alienlist[row][-i] != None:
                    answer.append(alienlist[row][-i])

#Helper functions to find the rightmost and leftmost collumns
    def _alienColList(alienlist):
        """
        returns a list of 0's and 1's. A 0 means there are no aliens left in the
        collumn

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        collumns = []
        for col in range(ALIENS_IN_ROW):
            x = 0
            for row in range(ALIEN_ROWS):
                if alienlist[row][col] != None:
                    x = x + 1
            if x != 0:
                collumns.append(1)
            else:
                collumns.append(0)
        return collumns

    def _aliens_left_collumn(alienlist):
        """
        find the number of the collumn of aliens furthest to the left

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        collumns = Wave._alienColList(alienlist)
        for x in range(len(collumns)):
            if collumns[x] == 1:
                return x

    def _aliens_right_collumn(alienlist):
        """
        returns the number of the rightmost collumn that has at least one Alien
        object. If the collums started with the number 1 from the rightmost
        collumn and counted up as you move left.

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        collumns = Wave._alienColList(alienlist)
        for x in range(len(collumns)):
            x = x + 1
            if collumns[-x] == 1:
                return x

    def _alien_from_left_col(alienlist):
        """
        returns an Alien from the leftmost collumn. Used to see if the alien
        wave reaches the edge of the screen

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        for row in range(ALIEN_ROWS):
            col = Wave._aliens_left_collumn(alienlist)
            if alienlist[row][col] != None:
                return alienlist[row][col]

    def _alien_from_right_col(alienlist):
        """
        returns an Alien from the rightmost collumn. Used to see if the alien
        wave reaches the edge of the screen

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        for row in range(ALIEN_ROWS):
            col = Wave._aliens_right_collumn(alienlist)
            if alienlist[row][-col] != None:
                return alienlist[row][-col]

    def aliensGone(alienlist):
        """
        returns an empty list if all of the aliens have been set to None,
        otherwise returns the given list

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if alienlist[row][col] != None:
                    return alienlist
        return []
#Helper methods to find the bottom row

    def _alien_row_empty(alienrow):
        """
        returns True if all aliens in a row are None

        Parameter alienrow: The alien row to be examined
        Precondition: alienrow is a list of aliens
        """
        for x in alienrow:
            if x != None:
                return False
        return True

    def _alien_bottom_row(alienlist):
        """
        returns the bottom row of the alien list that has at least one alien

        Parameter alienlist: the list of aliens to be checked
        Precondition: alienlist is a 2D list of Alien objects or None if the
        alien has been deleted
        """
        x = ALIEN_ROWS-1
        while Wave._alien_row_empty(alienlist[x]):
            x = x - 1
        return alienlist[x]

    def _alien_from_row(alienrow):
        """
        returns the first non-None Alien object in a row

        Parameter alienrow: The alien row to be examined
        Precondition: alienrow is a list of aliens
        """
        x = 0
        while alienrow[x] == None:
            x = x + 1
        return alienrow[x]
