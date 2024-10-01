import json_cpp
from json_cpp import JsonObject, JsonList
from .util import *
import math


class Location(JsonObject):

    def __init__(self,
                 x: float = 0.0,
                 y: float = 0.0):
        self.x = float(x)
        self.y = float(y)

    def __hash__(self):
        hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def __add__(self, o):
        c = Location()
        c.x = self.x + o.x
        c.y = self.y + o.y
        return c

    def __sub__(self, o):
        c = Location()
        c.x = self.x - o.x
        c.y = self.y - o.y
        return c

    def move(self, theta: float, dist: float):
        self.x += math.sin(theta) * dist
        self.y += math.cos(theta) * dist
        return self

    def atan(self, location = None) -> float:
        if location is None:
            return math.atan2(self.x, self.y)
        v = location-self
        return math.atan2(v.x, v.y)

    def mod(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def dist(self, location=None, segment: tuple = None) -> float:
        if location:
            check_type(location, Location, "incorrect type for location")
            v = location-self
            return (v.x ** 2 + v.y ** 2) ** .5
        elif segment:
            check_type(segment, tuple, "incorrect type for segment")
            line_start, line_end = segment
            check_type(line_start, Location, "incorrect type for line_start")
            check_type(line_end, Location, "incorrect type for line_end")
            normal_length = line_end.dist(line_start)
            distance = ((self.x - line_start.x) * (line_end.y - line_start.y) - (self.y - line_start.y) * (line_end.x - line_start.x)) / normal_length
            return abs(distance)

    def __mul__(self, multiplier):
        if isinstance(multiplier, Location):
            return Location(self.x*multiplier.x, self.y*multiplier.y)
        return Location(self.x * multiplier, self.y * multiplier)

    def __rmul__(self, multiplier):
        if isinstance(multiplier, Location):
            return Location(self.x*multiplier.x, self.y*multiplier.y)
        return Location(self.x * multiplier, self.y * multiplier)

class Scale (Location):
    def __init__(self,
                 x: float = 0.0,
                 y: float = 0.0):
        Location.__init__(self, x=x, y=y)

class Location_list(JsonList):

    def __init__(self, iterable=None, allow_empty=False):
        JsonList.__init__(self, iterable=iterable, list_type=Location, allow_empty=allow_empty)

    def get_x(self):
        x = []
        for location in self:
            x.append(location.x)
        return x

    def get_y(self):
        y = []
        for location in self:
            y.append(location.y)
        return y

    def total_distance(self) -> float:
        return self.distance_from_start()[-1]

    def distance_from_start(self) -> list:
        ds = JsonList(list_type=float)
        d = 0
        ll = self[0]
        for l in self:
            if ll is not None:
                d += l.dist(ll)
                ds.append(d)
                ll = l
        return ds


def segments_intersect(segment1: tuple, segment2: tuple):
    segment1_point1, segment1_point2 = segment1
    segment2_point1, segment2_point2 = segment2
    t1 = segment1_point1.atan(segment1_point2)
    t11 = segment1_point1.atan(segment2_point1)
    t12 = segment1_point1.atan(segment2_point2)
    if not angle_between(t1, t11, t12):
        return False
    t2 = segment2_point1.atan(segment2_point2)
    t21 = segment2_point1.atan(segment1_point1)
    t22 = segment2_point1.atan(segment1_point2)
    if not angle_between(t2, t21, t22):
        return False
    return True
