from package import Package
from container import Container
from itertools import permutations
from functools import cmp_to_key

TREE_WIDTH = 5


def greaterPair(a: tuple[float, Container], b: tuple[float, Container]):
    if a[0] > b[0]:
        return -1
    elif a[0] < b[0]:
        return 1
    else:
        if a[1].itemCount() < b[1].itemCount():
            return -1
        elif a[1].itemCount() > b[1].itemCount():
            return 1
    return 0


class Packer():
    def __init__(self, packages: list[Package] = [], containers: list[Container] = []) -> None:
        self.packages = packages
        self.containers = containers

    def pack(self):
        totalVolOpt = 0
        for cont in self.containers:
            cont = self.three_d_pack(cont, self.packages)
            totalVolOpt += cont.outputRep()
        return totalVolOpt/len(self.containers)

    def allowed_orientations(self, I: Package) -> list[Package]:
        Iarr: list[Package] = [None for _ in range(6)]

        if I.orientation[0] == 1:  # l is vertical
            # h x b
            Iarr[0] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.h,
                b1=I.b,
                h1=I.l,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[0].vert_load_lim = I.stackLoad[0]

            # b x h
            Iarr[1] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.b,
                b1=I.h,
                h1=I.l,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[1].vert_load_lim = I.stackLoad[0]

        if I.orientation[1] == 1:  # b is vertical
            # l x h
            Iarr[2] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.l,
                b1=I.h,
                h1=I.b,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[2].vert_load_lim = I.stackLoad[1]

            # h x l
            Iarr[3] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.h,
                b1=I.l,
                h1=I.b,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[3].vert_load_lim = I.stackLoad[1]

        if I.orientation[2] == 1:  # h is vertical
            # l x b
            Iarr[4] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.l,
                b1=I.b,
                h1=I.h,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[4].vert_load_lim = I.stackLoad[2]

            # b x l
            Iarr[5] = Package(
                l=I.l, b=I.b, h=I.h,
                l1=I.b,
                b1=I.l,
                h1=I.h,
                dest=I.dest,
                orientation=I.orientation,
                stackLoad=I.stackLoad)
            Iarr[5].vert_load_lim = I.stackLoad[2]

        return Iarr

    def print_res(self, C: Container):
        C.print_obj()
        for pack in C.packedItems:
            s = "\t{} {} {}"
            print("\t{}".format(pack.dest))
            print(s.format(pack.l, pack.b, pack.h))
            print(s.format(pack.l1, pack.b1, pack.h1))
            print(s.format(pack.pos.x, pack.pos.y, pack.pos.z))
            print()

    def three_d_pack(self, C: Container, items: list[Package]):
        options: list[tuple[float, Container]] = []
        options.append((self.greedy_pack(C, items, len(items) - 1), C))
        for i in range(len(items)):
            s = " ".join(str(x[0]) for x in options)
            print(s)

            I = items[i]
            Iarr = self.allowed_orientations(I)

            for k in range(len(options) - 1, -1, -1):
                opt = options[k]
                C = opt[1]
                options.append((self.greedy_pack(C, items, len(items) - 1), C))
                for j in range(6):
                    if Iarr[j] is None:
                        continue

                    Iarr[j].pos = options[k][1].fit(
                        Iarr[j].l1, Iarr[j].b1, Iarr[j].h1, Iarr[j].stress_load())
                    if Iarr[j].pos.x != -1:
                        C = options[k][1]
                        C = self.pack_item(C, Iarr[j])
                        options.append((self.greedy_pack(C, items, i - 1), C))
                del options[k]
            options.sort(key=cmp_to_key(greaterPair))
            if len(options) > TREE_WIDTH:
                options = options[:TREE_WIDTH]

        self.print_res(C)
        return C

    def greedy_pack(self, C: Container, items: list[Package], starting):
        for i in range(starting, -1, -1):
            I = items[i]
            Iarr = self.allowed_orientations(I)
            for j in range(6):
                if Iarr[j] is None:
                    continue

                Iarr[j].pos = C.fit(Iarr[j].l1, Iarr[j].b1,
                                    Iarr[j].h1, Iarr[j].stress_load())
                if Iarr[j].pos.x != -1:
                    C = self.pack_item(C, Iarr[j])
                    break

        return C.volOpt()

    def pack_item(self, C: Container, I: Package) -> Container:
        if I.pos.x == -1:
            return

        load = I.stress_load()
        for m in range(I.pos.x, I.pos.x + I.l1, 1):
            for n in range(I.pos.y, I.pos.y + I.b1, 1):
                C.h_grid[m][n] += I.h1
                C.load_grid[m][n] += load
                if C.load_lim[m][n] == -1:
                    C.load_lim[m][n] = I.vert_load_lim
                else:
                    C.load_lim[m][n] = min(
                        C.load_lim[m][n] - load, I.vert_load_lim)

        if I.pos.x + I.l1 < C.L:
            C.positions.add((I.pos.x + I.l1, I.pos.y))

        if I.pos.y + I.b1 < C.B:
            C.positions.add((I.pos.x, I.pos.y + I.b1))

        I.packed = True
        C.packedItems.append(I)

        return C
