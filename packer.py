from package import Package, make_package_copy, allowed_orientations
from container import Container, make_container_copy
from functools import cmp_to_key
import random

TREE_WIDTH = 5


def greater_pair(a: tuple[float, Container], b: tuple[float, Container]):
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
        total_vol_opt = 0
        for cont in self.containers:
            cont = self.three_d_pack(cont, self.packages)
            total_vol_opt += cont.output_rep()
        return total_vol_opt/len(self.containers)

    def print_res(self, C: Container):
        C.print_obj()
        for pack in C.packed_items:
            s = "\t{} {} {}"
            print("\t{}".format(pack.dest))
            print(s.format(pack.l, pack.b, pack.h))
            print(s.format(pack.l1, pack.b1, pack.h1))
            print(s.format(pack.pos.x, pack.pos.y, pack.pos.z))
            print()

    def three_d_pack(self, C: Container, items: list[Package]):
        options: list[tuple[float, Container]] = []
        options.append((self.greedy_pack(C, items, len(items) - 1), C))

        for i in range(len(items) - 1, -1, -1):

            I = items[i]
            Iarr = allowed_orientations(I)
            # random.shuffle(Iarr)

            for k in range(len(options) - 1, -1, -1):
                C_new = make_container_copy(options[k][1])
                options.append((self.greedy_pack(C_new, items, i - 1), C_new))

                for j in range(6):
                    if Iarr[j] is None:
                        continue

                    Iarr[j].pos = options[k][1].fit(
                        Iarr[j].l1, Iarr[j].b1, Iarr[j].h1, Iarr[j].stress_load())

                    if Iarr[j].pos.x != -1:
                        C_new = make_container_copy(options[k][1])
                        C_new = self.pack_item(C_new, Iarr[j])
                        options.append(
                            (self.greedy_pack(C_new, items, i - 1), C_new))

                del options[k]

            options.sort(key=cmp_to_key(greater_pair))

            if len(options) > TREE_WIDTH:
                options = options[:TREE_WIDTH]

            s = " ".join(str(round(x[0], 3)) for x in options)
            print("s - ", s)

        return options[0][1]

    def greedy_pack(self, C: Container, items: list[Package], starting):
        C1 = make_container_copy(C)
        for i in range(starting, -1, -1):
            I = items[i]
            Iarr = allowed_orientations(I)

            for j in range(6):
                if Iarr[j] is None:
                    continue

                Iarr[j].pos = C1.fit(Iarr[j].l1, Iarr[j].b1,
                                     Iarr[j].h1, Iarr[j].stress_load())
                if Iarr[j].pos.x != -1:
                    C1 = self.pack_item(C1, Iarr[j])
                    break

        return C1.vol_opt()

    def pack_item(self, C: Container, I: Package) -> Container:
        if I.pos.x == -1:
            return

        load = I.stress_load()
        for m in range(I.pos.x, I.pos.x + I.l1, 1):
            for n in range(I.pos.y, I.pos.y + I.b1, 1):
                C.h_grid[m][n] += I.h1
                C.load_grid[m][n] += load
                C.load_lim[m][n] = min(
                    C.load_lim[m][n] - load, I.vert_load_lim)

        if I.pos.x + I.l1 < C.L:
            C.positions.add((I.pos.x + I.l1, I.pos.y))

        if I.pos.y + I.b1 < C.B:
            C.positions.add((I.pos.x, I.pos.y + I.b1))

        if I.pos.z + I.h1 < C.H:
            C.positions.add((I.pos.x, I.pos.y))

        I.packed = True
        C.packed_items.append(I)

        return C
