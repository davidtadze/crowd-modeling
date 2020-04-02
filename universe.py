import sys
import array
import draw
from body import Body 
from instream import InStream
from vector import Vector
import time

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
    
    def increaseTime(self, dt):
        n = len(self._bodies)
        f = array.create1D(n, Vector([0, 0]))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    bodyi = self._bodies[i]
                    bodyj = self._bodies[j]
                    f[i] = f[i] + bodyi.forceFrom(bodyj)

        for i in range(n):
            self._bodies[i].move(f[i], dt)    

    def draw(self):
        for body in self._bodies:
            body.draw()

#-----------------------------------------------------------------------

def main():
    filename = sys.argv[1]
    dt = float(sys.argv[2])
    universe = Universe(filename)
    while True:
        universe.increaseTime(dt)
        draw.clear()
        universe.draw()
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