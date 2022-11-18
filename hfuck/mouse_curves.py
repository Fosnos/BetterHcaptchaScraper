from math import ceil; from random import choice, randint
from time import time; from typing import Tuple


def _bezier(xys, ts):
    result = []
    for t in ts:
        tpowers = (t ** i for i in range(4))
        upowers = reversed([(1 - t) ** i for i in range(4)])
        coefs = [c * a * b for c, a, b in zip([1, 3, 3, 1], tpowers, upowers)]
        result.append(list(sum([coef * p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
    return result

def mouse_curve(start_pos, end_pos, ln):
    ts = [t / ln for t in range(int(ln / 100 * 101))]
    control_1 = (start_pos[0] + choice((-1, 1)) * abs(ceil(end_pos[0]) - ceil(start_pos[0])) * 0.01 * 3,
                 start_pos[1] + choice((-1, 1)) * abs(ceil(end_pos[1]) - ceil(start_pos[1])) * 0.01 * 3)
    control_2 = (start_pos[0] + choice((-1, 1)) * abs(ceil(end_pos[0]) - ceil(start_pos[0])) * 0.01 * 3,
                 start_pos[1] + choice((-1, 1)) * abs(ceil(end_pos[1]) - ceil(start_pos[1])) * 0.01 * 3)
    xys = [start_pos, control_1, control_2, end_pos]
    points = _bezier(xys, ts)
    return [[ceil(x), ceil(y)] for x, y, in points]


class MotionData:
    def __init__(self, x=0, y=0, controller=None):
        self._point = (x, y)
        self._meanPeriod = 0
        self._meanCounter = 0
        self._data = []
        self._controller = controller

    @property
    def timestamp(self):
        return self._controller.timestamp

    @timestamp.setter
    def timestamp(self, val):
        self._controller.timestamp = val

    def moveTo(self, x, y, s):
        curve = mouse_curve(self._point, (x, y), s)
        for pt in curve:
            self.addPoint(*pt)
        self._point = self._data[-1][:2]

    def addPoint(self, x, y):
        self.timestamp += randint(20, 40)
        self._data.append([x, y, self.timestamp])
        if self._meanCounter != 0:
            delta = self._data[-1][2] - self._data[-2][2]
            self._meanPeriod = (self._meanPeriod * self._meanCounter + delta) / (self._meanCounter + 1)
        self._meanPeriod += 1

    @property
    def data(self):
        return self._data

    @property
    def mp(self):
        return self._meanPeriod

    @property
    def point(self):
        return self._point

class MotionController:
    def __init__(self, timestamp: int, start_point: Tuple[int, int]):
        self.timestamp = timestamp or time()
        self._mm = MotionData(*start_point, controller=self)
        self._md = MotionData(controller=self)
        self._mu = MotionData(controller=self)

        self._lastPoint = start_point

    def move(self, x, y, s):
        self._mm.moveTo(x, y, s)
        self._lastPoint = self._mm.point

    def click(self, x=0, y=0):
        if not x and not y:
            x, y = self._lastPoint
        self._md.addPoint(x, y)
        self._mu.addPoint(x, y)
        self._lastPoint = (x, y)

    def get(self, mm=True, md=True, mu=True):
        r = {}
        if mm:
            r["mm"] = self._mm.data
            r["mm-mp"] = self._mm.mp
        if md:
            r["md"] = self._md.data
            r["md-mp"] = self._md.mp
        if mu:
            r["mu"] = self._mu.data
            r["mu-mp"] = self._mu.mp
        return r