from util import array
from util.vector import Vector
import body

class PhysicsSystem:
    def _move(self, body, f, dt):
        a = f.scale(1 / body._mass)
        body._v = body._v + (a.scale(dt))
        body._r = body._r + body._v.scale(dt)

    def _forceFrom(self, body, other):
        G = 6.67e-11
        delta = other._r - body._r
        dist = abs(delta)
        magnitude = (G * body._mass * other._mass) / (dist * dist)
        f = delta.direction().scale(magnitude)
        return f

    def increaseTime(self, bodies, dt):
        n = len(bodies)
        f = array.create1D(n, Vector([0, 0]))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    bodyi = bodies[i]
                    bodyj = bodies[j]
                    f[i] = f[i] + self._forceFrom(bodyi, bodyj)

        for i in range(n):
            self._move(bodies[i], f[i], dt)
        
        return bodies