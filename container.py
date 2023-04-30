from package import Package, Location
import copy
import numpy as np
import cupy as cp

MAXV = 1000000000


class Container:
    def __init__(self,
                 x=0,
                 y=0,
                 z=0,
                 ID=0,
                 max_wt=0,
                 consignment_ids: list[int] = [],
                 packed_items: list[Package] = []) -> None:
        self.L = x
        self.B = y
        self.H = z
        self.ID = ID

        self.consignment_ids = consignment_ids

        l = [[0 for _ in range(self.B)] for _ in range(self.L)]
        load_lim = [[MAXV for _ in range(self.B)] for _ in range(self.L)]
        self.h_grid = cp.array(l, dtype='int32')
        self.load_grid = cp.array(l, dtype='double')
        self.load_lim = cp.array(load_lim, dtype='double')
        
        self.positions = {(0, 0)}
        self.packed_items = packed_items

        self.max_wt = max_wt
        self.vol = self.L * self.B * self.H

    def print_obj(self):
        print(self.L, self.B, self.H)

    def fit(self, l, b, h, stress_load):
        # finds a fit and returns
        loc = Location()
        pos_valid = False

        for p in self.positions:

            x = p[0]
            y = p[1]
            base = self.h_grid[x][y].item()
            # print(base)

            if x + l > self.L or y + b > self.B or base + h > self.H:
                continue

            h_in_range = self.h_grid[x:x+l, y:y+b]
            base_equal = cp.all(h_in_range == base).item()
            if base_equal is True:
                load_in_range = self.load_lim[x:x+l, y:y+b]
                load_allowed = cp.all(stress_load <= load_in_range).item()
                if load_allowed is True:
                    pos_valid = True

            if pos_valid:
                loc = Location(x, y, base)
                break

        # loc.print_loc()

        if loc.x < 0:
            return Location()

        return loc

    def vol_opt(self):
        pVol = 0
        for pack in self.packed_items:
            pVol += pack.vol

        return pVol/self.vol

    def output_rep(self):
        op = "Volume Optimization {vol_opt}, Item Count {ic}".format(
            vol_opt=self.vol_opt(), ic=self.itemCount())
        print(op)
        return self.vol_opt()

    def reset(self):
        self.positions.clear()
        self.positions = {(0, 0)}

        l = [[0 for _ in range(self.B)] for _ in range(self.L)]
        load_lim = [[MAXV for _ in range(self.B)] for _ in range(self.L)]
        self.h_grid = cp.array(l, dtype='int32')
        self.load_grid = cp.array(l, dtype='double')
        self.load_lim = cp.array(load_lim, dtype='double')

        self.packed_items.clear()

    def itemCount(self):
        return len(self.packed_items)


def make_container_copy(C: Container):
    C1 = Container(x=C.L,
                   y=C.B,
                   z=C.H,
                   ID=C.ID,
                   max_wt=C.max_wt,
                   packed_items=C.packed_items.copy())
    # C1.h_grid = copy.deepcopy(C.h_grid)
    # C1.load_grid = copy.deepcopy(C.load_grid)
    # C1.load_lim = copy.deepcopy(C.load_lim)
    # C1.positions = copy.deepcopy(C.positions)

    C1.h_grid = cp.copy(C.h_grid)
    C1.load_grid = cp.copy(C.load_grid)
    C1.load_lim = cp.copy(C.load_lim)
    C1.positions = copy.deepcopy(C.positions)

    return C1
