
import math


class Location:
    """ location class """

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

    def print_loc(self):
        print("({x}, {y}, {z})".format(x=self.x, y=self.y, z=self.z))


class Package:
    """ package class """

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
                 stack_load=[],
                 stackable=False,
                 pos=Location(),
                 orientation=[0 for _ in range(3)],
                 ) -> None:
        self.l = l
        self.b = b
        self.h = h

        self.packed: bool = packed
        self.stack_load = stack_load
        self.stackable = stackable

        self.l1 = l1
        self.b1 = b1
        self.h1 = h1

        self.vert_load_lim = stack_load[2]

        self.ID = ID
        self.wt = wt
        self.dest = dest

        self.vol = self.l * self.b * self.h
        self.max_dim = max([self.l, self.b, self.h])

        self.pos: Location = pos
        self.orientation = orientation

    def print_obj(self):
        print(self.dest, self.ID, self.max_dim)

    def set_pack_dim(self, l, b, h):
        self.l1 = l
        self.b1 = b
        self.h1 = h

    def stress_load(self):
        base_area = self.l1 * self.b1
        return self.wt/base_area


def cmp_pack(pa: Package, pb: Package):
    """ sorts by destination then maximum load possible """
    if pa.dest < pb.dest:
        return -1
    elif pa.dest > pb.dest:
        return 1
    else:
        m1 = max([pa.orientation[i] * pa.stack_load[i] for i in range(3)])
        m2 = max([pb.orientation[i] * pb.stack_load[i] for i in range(3)])
        if m1 < m2:
            return -1
        elif m1 > m2:
            return 1
        else:
            return 0


def make_package_copy(I: Package):
    """ returns a new package obj with same values """
    I1 = Package(ID=I.ID,
                 wt=I.wt,
                 dest=I.dest,
                 l=I.l,
                 b=I.b,
                 h=I.h,
                 l1=I.l1,
                 b1=I.b1,
                 h1=I.h1,
                 packed=I.packed,
                 stack_load=I.stack_load,
                 stackable=I.stackable,
                 pos=I.pos,
                 orientation=I.orientation)
    return I1


def allowed_orientations(I: Package) -> list[Package]:
    """ returns a list with allowed orientations of I """
    Iarr: list[Package] = [None for _ in range(6)]

    if I.orientation[0] == 1:  # l is vertical
        # h x b
        Iarr[0] = make_package_copy(I)
        Iarr[0].set_pack_dim(I.h, I.b, I.l)
        Iarr[0].vert_load_lim = I.stack_load[0]

        # b x h
        Iarr[1] = make_package_copy(I)
        Iarr[1].set_pack_dim(I.b, I.h, I.l)
        Iarr[1].vert_load_lim = I.stack_load[0]

    if I.orientation[1] == 1:  # b is vertical
        # l x h
        Iarr[2] = make_package_copy(I)
        Iarr[2].set_pack_dim(I.l, I.h, I.b)
        Iarr[2].vert_load_lim = I.stack_load[1]

        # h x l
        Iarr[3] = make_package_copy(I)
        Iarr[3].set_pack_dim(I.h, I.l, I.b)
        Iarr[3].vert_load_lim = I.stack_load[1]

    if I.orientation[2] == 1:  # h is vertical
        # l x b
        Iarr[4] = make_package_copy(I)
        Iarr[4].set_pack_dim(I.l, I.b, I.h)
        Iarr[4].vert_load_lim = I.stack_load[2]

        # b x l
        Iarr[5] = make_package_copy(I)
        Iarr[5].set_pack_dim(I.b, I.l, I.h)
        Iarr[5].vert_load_lim = I.stack_load[2]

    return Iarr
