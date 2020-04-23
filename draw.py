import time
import os

from util import color

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame
import pygame.gfxdraw

from util.color import WHITE
from util.color import BLACK
from util.color import RED
from util.color import GREEN
from util.color import BLUE
from util.color import GRAY

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

_canvas_width = float(_DEFAULT_CANVAS_SIZE)
_canvas_height = float(_DEFAULT_CANVAS_SIZE)

_background = None
_surface = None

_window_created = False

def _pygame_color(c):
    r = c._r
    g = c._g
    b = c._b
    return pygame.Color(r, g, b)

def _scale_x(x):
    return _canvas_width * (x - _xmin) / (_xmax - _xmin)

def _scale_y(y):
    return _canvas_height * (_ymax - y) / (_ymax - _ymin)

def _factor_x(w):
    return w * _canvas_width / abs(_xmax - _xmin)

def _factor_y(h):
    return h * _canvas_height / abs(_ymax - _ymin)

def init(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    global _background
    global _surface
    global _canvas_width
    global _canvas_height
    global _window_created

    if _window_created:
        raise Exception('the draw window already was created')
    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')

    pygame.init()

    _canvas_width = w
    _canvas_height = h

    _background = pygame.display.set_mode((w, h))
    _surface = pygame.Surface((w, h))

    _window_created = True

def set_x_scale(min=_DEFAULT_XMIN, max=_DEFAULT_XMAX):
    global _xmin
    global _xmax

    min = float(min)
    max = float(max)

    if min >= max:
        raise Exception('min must be less than max')

    size = max - min
    _xmin = min - _BORDER * size
    _xmax = max + _BORDER * size

def set_y_scale(min=_DEFAULT_YMIN, max=_DEFAULT_YMAX):
    global _ymin
    global _ymax

    min = float(min)
    max = float(max)

    if min >= max:
        raise Exception('min must be less than max')

    size = max - min
    _ymin = min - _BORDER * size
    _ymax = max + _BORDER * size

def _make_sure_window_created():
    global _window_created
    if not _window_created:
        init()
        _window_created = True

def _check_for_events():
    _make_sure_window_created()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def _pixel(x, y, color=BLACK):
    _make_sure_window_created()

    xs = _scale_x(x)
    xy = _scale_y(y)

    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(xy)),
        _pygame_color(color)
    )

def line(r1, r2, color=BLACK):
    _make_sure_window_created()

    r1_scaled = (_scale_x(r1[0]), _scale_y(r1[1]))
    r2_scaled = (_scale_x(r2[0]), _scale_y(r2[1]))

    pygame.draw.line(_surface, _pygame_color(color), r1_scaled, r2_scaled)

def filled_circle(x, y, r, color=BLACK):
    _make_sure_window_created()
    
    x = float(x)
    y = float(y)
    r = float(r)

    rs = _factor_x(r)

    if (rs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scale_x(x)
        ys = _scale_y(y)
        pygame.draw.circle(_surface, _pygame_color(color), (xs, ys), rs)

def clear(c=WHITE):
    _make_sure_window_created() 
    
    _surface.fill(_pygame_color(c))

def save(f):
    _make_sure_window_created()

    pygame.image.save(_surface, f)

def show(msec):
    _make_sure_window_created()

    _background.blit(_surface, (0, 0))
    pygame.display.flip()

    _check_for_events()

    QUANTUM = .1
    sec = msec / 1000.0
    if sec < QUANTUM:
        time.sleep(sec)
        return
    secondsWaited = 0.0
    while secondsWaited < sec:
        time.sleep(QUANTUM)
        secondsWaited += QUANTUM
        _check_for_events()

set_x_scale()
set_y_scale()