import math
class V2:
    def __init__(self,x,y):
        self._x = x
        self._y = y

    @property
    def tuple(self):
        return (self._x,self._y)

    @property
    def mag2(self):
        return self._x ** 2 + self._y ** 2

    @property
    def mag(self):
        return math.sqrt(self.mag2)
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def normalise(self):
        mg = self.mag
        if mg == 0: return V2(self._x,self._x)
        self._x /= mg
        self._y /= mg
        return V2(self._x, self._y)
    
    def __add__(self, other):
        if isinstance(other, V2):
            return V2(self._x + other.x, self._y + other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return V2(self._x + other, self._y + other)
        else:
            raise NotImplementedError

    def __mul__(self,other):
        if isinstance(other, V2):
            return V2(self._x * other.x, self._y * other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return V2(self._x * other, self.y * other)
        else:
            raise NotImplementedError

    def __sub__(self, other):
        if isinstance(other, V2):
            return V2(self._x - other.x, self._y - other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return V2(self._x - other, self._y - other)
        else:
            raise NotImplementedError

    def __truediv__(self,other):
        if isinstance(other, V2):
            return V2(self._x / other.x, self._y / other.y)
        elif isinstance(other, int) or isinstance(other, float):
            return V2(self._x / other, self.y / other)
        else:
            raise NotImplementedError
    __rmul__ = __mul__
    def __str__(self):
        return f"V2({self.x},{self.y})"
    