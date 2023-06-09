from package import Package, Location
import copy
import numpy as np

MAXV = 1e9


class Container:
    """ class for Container """

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

        l1 = [[0 for _ in range(self.B)] for _ in range(self.L)]
        l2 = [[0 for _ in range(self.B)] for _ in range(self.L)]
        load_lim = [[MAXV for _ in range(self.B)] for _ in range(self.L)]
        
        # height to which container is packed
        self.h_grid = np.array(l1, dtype='int32')

        # load on the container
        self.load_grid = np.array(l2, dtype='double')

        # load limit of the container
        self.load_lim = np.array(load_lim, dtype='double')

        self.positions = {(0, 0)}
        self.packed_items = packed_items

        self.max_wt = max_wt
        self.vol = self.L * self.B * self.H

    def print_obj(self):
        print(self.L, self.B, self.H)

    def fit(self, l, b, h, stress_load):
        """ finds a fit and returns """
        loc = Location()

        for p in self.positions:
            pos_valid = True
            x = p[0]
            y = p[1]
            base = self.h_grid[x][y].item()

            if x + l > self.L or y + b > self.B or base + h > self.H:
                continue
            
            # checking if base is equal
            h_in_range = self.h_grid[x:x+l, y:y+b]
            base_equal = np.all(h_in_range == base).item()
            if base_equal is False:
                continue
            
            # checking if load is below limit
            load_in_range = self.load_lim[x:x+l, y:y+b]
            load_allowed = np.all(stress_load <= load_in_range).item()
            if load_allowed is False:
                continue

            if pos_valid:
                loc = Location(x, y, base)
                break

        if loc.x < 0:
            return Location()

        return loc

    def vol_opt(self):
        """ returns volume utilisation """
        pVol = 0
        for pack in self.packed_items:
            pVol += pack.vol

        return pVol/self.vol

    def output_rep(self):
        op = "Volume Optimization {vol_opt}, Item Count {ic}".format(
            vol_opt=self.vol_opt(), ic=self.item_count())
        print(op)
        return self.vol_opt()

    def reset(self):
        self.positions.clear()
        self.positions = {(0, 0)}

        l = [[0 for _ in range(self.B)] for _ in range(self.L)]
        load_lim = [[MAXV for _ in range(self.B)] for _ in range(self.L)]
        self.h_grid = np.array(l, dtype='int32')
        self.load_grid = np.array(l, dtype='double')
        self.load_lim = np.array(load_lim, dtype='double')

        self.packed_items.clear()

    def item_count(self):
        return len(self.packed_items)


def make_container_copy(C: Container):
    """ returns a new container obj with same values """
    C1 = Container(x=C.L,
                   y=C.B,
                   z=C.H,
                   ID=C.ID,
                   max_wt=C.max_wt,
                   packed_items=copy.deepcopy(C.packed_items))

    C1.h_grid = np.copy(C.h_grid)
    C1.load_grid = np.copy(C.load_grid)
    C1.load_lim = np.copy(C.load_lim)
    C1.positions = copy.deepcopy(C.positions)

    return C1
