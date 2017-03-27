import math

class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x;
        self.y = y;

        def __str__(self):
            return "({},{})".format(self.x, self.y)

class Line(object):
    def __init__(self, start = Point(), end = Point()):
        self.start = start;
        self.end = end;
        self.xcurr = 0

    @property
    def magnitude(self):
        return math.sqrt( self.deltaX**2 + self.deltaY**2 )

    @property 
    def deltaX(self):
        return self.end.x - self.start.x

    @property
    def deltaY(self):
        return self.end.y - self.start.y

    @property
    def slope(self):
        return self.deltaY/self.deltaX

    @property
    def iterx(self):
        return self.start.x

    def __iter__(self):
        self.xcurr = self.iterx
        return self

    def __next__(self): 
        if self.xcurr > self.end.x:
            raise StopIteration
        else:
            self.xcurr += 1
            return self.xcurr, self.start.y

