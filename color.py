class Color:

    def __init__(self, r=0, g=0, b=0):
        self._r = r
        self._g = g
        self._b = b

    #-------------------------------------------------------------------

    def getRed(self):
        return self._r

    def getGreen(self):
        return self._g
    
    def getBlue(self):
        return self._b

    #-------------------------------------------------------------------

    def __str__(self):
        return '(' + str(self._r) + ', ' + str(self._g) + ', ' + \
            str(self._b) + ')'

#-----------------------------------------------------------------------

WHITE      = Color(255, 255, 255)
BLACK      = Color(  0,   0,   0)

RED        = Color(255,   0,   0)
GREEN      = Color(  0, 255,   0)
BLUE       = Color(  0,   0, 255)

CYAN       = Color(  0, 255, 255)
MAGENTA    = Color(255,   0, 255)
YELLOW     = Color(255, 255,   0)

GRAY       = Color(128, 128, 128)

ORANGE     = Color(255, 200,   0)
VIOLET     = Color(238, 130, 238)
PINK       = Color(255, 175, 175)