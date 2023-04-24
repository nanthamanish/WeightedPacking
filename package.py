
import math


class Location:
    def __init__(self, x=-1, y=-1, z=-1):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, l1) -> float:
        dist = pow(self.x - l1.x, 2)
        dist += pow(self.y - l1.y, 2)
        dist += pow(self.z - l1.z, 2)
        dist = math.sqrt(dist)
        return dist

    def printLoc(self):
        print("({x}, {y}, {z})".format(x=self.x, y=self.y, z=self.z))


class Package:
    def __init__(self,
                 ID=0,
                 wt=0,
                 dest=0,
                 l=0,
                 b=0,
                 h=0,
                 l1=0,
                 b1=0,
                 h1=0,
                 packed=False,
                 stackLoad=[],
                 stackable=False,
                 pos=Location(),
                 orientation=[0 for _ in range(3)],
                 ) -> None:
        self.l = l
        self.b = b
        self.h = h

        self.packed: bool = packed
        self.stackLoad = stackLoad
        self.stackable = stackable

        self.l1 = l1
        self.b1 = b1
        self.h1 = h1

        self.ID = ID
        self.wt = wt
        self.dest = dest

        self.pVol = self.l * self.b * self.h
        self.maxDim = max([self.l, self.b, self.h])

        self.pos: Location = pos
        self.orientation = orientation

    def print_obj(self):
        print(self.dest, self.ID, self.maxDim)
        # print(self.l, self.b, self.h)
        # print(self.orientation)
        # print(self.wt, self.pVol, self.stackLoad)

    def isBelow(self, item):
        res = self.pos.z + self.h <= item.pos.z and \
            (item.pos.x <= self.pos.x and self.pos.x <= item.pos.x + item.l or
             item.pos.x <= self.pos.x + self.l and self.pos.x + self.l <= item.pos.x + item.l) and \
            (item.pos.y <= self.pos.y and self.pos.y <= item.pos.y + item.b or
             item.pos.y <= self.pos.y + self.b and self.pos.y + self.b <= item.pos.y + item.b)
        return res

    def isBehind(self, item):
        res = self.pos.x + self.l < item.pos.x and \
            self.pos.z < item.pos.z + item.h and \
            (self.pos.y < item.pos.y and item.pos.y < self.pos.y + self.b or
             item.pos.y < self.pos.y and self.pos.y < item.pos.y + item.b)
        return res

    def isBlockedBy(self, item):
        res = self.isBelow(item) or self.isBehind(item)
        return res

    def setDim1(self, l, b, h):
        self.l1 = l
        self.b1 = b
        self.h1 = h
