import time
import os
import sys
import color
import string

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import pygame.gfxdraw
	
#-----------------------------------------------------------------------

from color import WHITE
from color import BLACK
from color import RED
from color import GREEN
from color import BLUE
from color import CYAN
from color import MAGENTA
from color import YELLOW
from color import GRAY
from color import ORANGE
from color import VIOLET
from color import PINK

#-----------------------------------------------------------------------

_BORDER = 0.0
_DEFAULT_XMIN = 0.0
_DEFAULT_XMAX = 1.0
_DEFAULT_YMIN = 0.0
_DEFAULT_YMAX = 1.0
_DEFAULT_CANVAS_SIZE = 512

_xmin = None
_ymin = None
_xmax = None
_ymax = None

_canvasWidth = float(_DEFAULT_CANVAS_SIZE)
_canvasHeight = float(_DEFAULT_CANVAS_SIZE)

_background = None
_surface = None

_windowCreated = False

#-----------------------------------------------------------------------

def _pygameColor(c):
    r = c.getRed()
    g = c.getGreen()
    b = c.getBlue()
    return pygame.Color(r, g, b)

#-----------------------------------------------------------------------

def _scaleX(x):
    return _canvasWidth * (x - _xmin) / (_xmax - _xmin)

def _scaleY(y):
    return _canvasHeight * (_ymax - y) / (_ymax - _ymin)

def _factorX(w):
    return w * _canvasWidth / abs(_xmax - _xmin)

def _factorY(h):
    return h * _canvasHeight / abs(_ymax - _ymin)

def setCanvasSize(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high.
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.
    """
    global _background
    global _surface
    global _canvasWidth
    global _canvasHeight
    global _windowCreated

    if _windowCreated:
        raise Exception('The stddraw window already was created')

    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')

    _canvasWidth = w
    _canvasHeight = h
    _background = pygame.display.set_mode([w, h])
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygameColor(WHITE))
    _windowCreated = True

def setXscale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    """
    Set the x-scale of the canvas such that the minimum x value
    is min and the maximum x value is max.
    """
    global _xmin
    global _xmax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def setYscale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    global _ymin
    global _ymax
    min = float(min)
    max = float(max)
    if min >= max:
        raise Exception('min must be less than max')
    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

#-----------------------------------------------------------------------

def _makeSureWindowCreated():
    global _windowCreated
    if not _windowCreated:
        setCanvasSize()
        _windowCreated = True

#-----------------------------------------------------------------------

def _pixel(x, y, color=BLACK):
    _makeSureWindowCreated()
    xs = _scaleX(x)
    xy = _scaleY(y)
    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(xy)),
        _pygameColor(color))

def circle(x, y, r, color=BLACK):
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(color),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs), 1)

def filledCircle(x, y, r, color=BLACK):
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0*r)
    hs = _factorY(2.0*r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(color),
            pygame.Rect(xs-ws/2.0, ys-hs/2.0, ws, hs),
            0)

#-----------------------------------------------------------------------

def clear(c=WHITE):
    _makeSureWindowCreated()
    _surface.fill(_pygameColor(c))

def save(f):
    _makeSureWindowCreated()
    pygame.image.save(_surface, f)

def show():
    _background.blit(_surface, (0, 0))
    pygame.display.flip()

#-----------------------------------------------------------------------

def _regressionTest():
    clear()

    circle(0.5, 0.5, .2)
    show()

    filledCircle(0.5, 0.5, .1)
    show()

    save("/Users/daviddavitadze/Downloads/img.jpg")

#-----------------------------------------------------------------------

setXscale()
setYscale()

#-----------------------------------------------------------------------

def _main():
    _regressionTest()

if __name__ == '__main__':
    _main()