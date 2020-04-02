import draw
import body

class RenderingSystem:
    def render(self, bodies):
        for body in bodies:
            draw.filledCircle(body._r[0], body._r[1], .1)