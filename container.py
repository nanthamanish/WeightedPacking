from package import Package, Location
import copy

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
        self.h_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.load_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.load_lim = [[-1 for _ in range(self.B)] for _ in range(self.L)]
        self.positions = {(0, 0)}
        self.packed_items = packed_items

        self.max_wt = max_wt
        self.vol = self.L * self.B * self.H

    def print_obj(self):
        print(self.L, self.B, self.H)

    def fit(self, l, b, h, stress_load):
        # finds a fit and returns
        loc = Location()
        pos_valid = True

        for p in self.positions:
            
            x = p[0]
            y = p[1]
            base = self.h_grid[x][y]

            if x + l > self.L or y + b > self.B or base + h > self.H:
                continue

            for m in range(l):
                for n in range(b):
                    if self.h_grid[x + m][y + n] != base:
                        pos_valid = False
                        break
                    elif self.load_lim[x + m][y + n] != -1 and self.load_lim[x + m][y + n] < stress_load:
                        pos_valid = False
                        break
                if pos_valid == False:
                    break

            if pos_valid:
                loc = Location(x, y, base)
                break

        if loc.x < 0:
            return Location()

        return loc

    def vol_opt(self):
        pVol = 0
        for pack in self.packed_items:
            pVol += pack.vol

        return pVol/self.vol

    def output_rep(self):
        op = "Volume Optimization {vol_opt} Item Count {ic}".format(
            vol_opt=self.vol_opt(), ic=self.itemCount())
        print(op)
        return self.vol_opt()

    def reset(self):
        self.positions.clear()
        self.positions = {(0, 0)}

        self.h_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]

        self.packed_items.clear()

    def itemCount(self):
        return len(self.packed_items)

def make_container_copy(C: Container):
    C1 = Container(x=C.L,
                 y=C.B,
                 z=C.H,
                 ID=C.ID,
                 max_wt=C.max_wt,
                 packed_items = C.packed_items.copy())
    C1.h_grid = copy.deepcopy(C.h_grid)
    C1.load_grid = copy.deepcopy(C.load_grid)
    C1.load_lim = copy.deepcopy(C.load_lim)
    C1.positions = copy.deepcopy(C.positions)

    return C1
