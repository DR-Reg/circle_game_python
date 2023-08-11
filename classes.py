from dataclasses import dataclass
import math
import pygame

################################### CLASSESS ###########################################
@dataclass(slots=True)
class V2:
    x: float
    y: float
    def __add__(a,b):
        if isinstance(a,V2) and isinstance(b, V2):
            return V2(a.x+b.x,a.y+b.y)
        else:
            return NotImplemented
    def __sub__(a,b):
        if isinstance(a,V2) and isinstance(b, V2):
            return V2(a.x-b.x,a.y-b.y)
        else:
            return NotImplemented

    @property
    def tuple(self):
        return self.x, self.y

    @property
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude
        self.x /= mag
        self.y /= mag

    def copy(self):
        return V2(self.x, self.y)

    def __mul__(self, val):
        if type(val) in [int, float]:
            return V2(self.x * val, self.y * val)
        else:
            return NotImplemented

class Line:
    def __init__(self, x1, y1, x2, y2, idx):
        self.p1 = V2(x1,y1)
        self.p2 = V2(x2,y2)
        self.idx = idx
    def draw(self, win, color, VCENT):
        pygame.draw.line(win, color, (VCENT + self.p1).tuple, (VCENT + self.p2).tuple)
    def get_intsect(self, line):
        if isinstance(line, Line):
            a1 = -self.m
            a2 = -line.m
            b1 = 1
            b2 = 1
            c1 = self.c
            c2 = line.c
            det = a1 * b2 - b1 * a2
            if det == 0:
                return None
            else:
                return V2(
                    (c1 * b2 - c2 * b1)/det,
                    (a1 * c2 - a2 * c1)/det
                )
        else:
            return NotImplemented
    @property
    def m(self):
        return (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
    @property
    def c(self):
        return self.p1.y - self.m * self.p1.x
