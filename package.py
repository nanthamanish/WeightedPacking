
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
        
        self.vert_load_lim = stackLoad[2]

        self.ID = ID
        self.wt = wt
        self.dest = dest

        self.vol = self.l * self.b * self.h
        self.maxDim = max([self.l, self.b, self.h])

        self.pos: Location = pos
        self.orientation = orientation

    def print_obj(self):
        print(self.dest, self.ID, self.maxDim)

    def setDim1(self, l, b, h):
        self.l1 = l
        self.b1 = b
        self.h1 = h

    def stress_load(self):
        base_area = self.l1 * self.b1
        return self.wt/base_area


def cmp_pack(pa: Package, pb: Package):
    if pa.dest == pb.dest:
        if pa.maxDim < pb.maxDim:
            return 1
        elif pa.maxDim > pb.maxDim: 
            return -1
        else:
            return 0
    
    elif pa.dest < pb.dest:
        return 1
    else:
        return -1