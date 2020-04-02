import sys
from util import array
import draw
from body import Body
from util.instream import InStream
from util.vector import Vector
import time

from physics_system import PhysicsSystem
from rendering_system import RenderingSystem

#-----------------------------------------------------------------------

class Universe:
    def __init__(self, filename):
        instream = InStream(filename)
        n = instream.readInt()
        radius = instream.readFloat()

        draw.setCanvasSize()

        draw.setXscale(-radius, +radius)
        draw.setYscale(-radius, +radius)

        self._bodies = array.create1D(n)
        for i in range(n):
            rx   = instream.readFloat()
            ry   = instream.readFloat()
            vx   = instream.readFloat()
            vy   = instream.readFloat()
            mass = instream.readFloat()
            r = Vector([rx, ry])
            v = Vector([vx, vy])
            self._bodies[i] = Body(r, v, mass)    

#-----------------------------------------------------------------------

def main():
    filename = sys.argv[1]
    dt = float(sys.argv[2])

    universe = Universe(filename)
    physics = PhysicsSystem()
    rendering = RenderingSystem()

    while True:
        universe._bodies = physics.increaseTime(universe._bodies, dt)
        draw.clear()
        rendering.render(universe._bodies)
        draw.show(10.0)

    # sec = 60
    # secondsWaited = 0.0
    # while secondsWaited < sec:
    #     universe.increaseTime(dt)
    #     universe.draw()
    #     draw.show(0.0)
    #     secondsWaited += dt

    draw.save("/Users/daviddavitadze/Downloads/universe.jpg")

if __name__ == '__main__':
    main()

#-----------------------------------------------------------------------

# python3 universe.py 4body.txt 20000