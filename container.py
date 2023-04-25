from package import Package, Location


class Container:
    def __init__(self,
                 x=0,
                 y=0,
                 z=0,
                 ID=0,
                 maxWt=0,
                 consignmentIDs: list[int] = [],
                 packedItems: list[Package] = []) -> None:
        self.L = x
        self.B = y
        self.H = z
        self.ID = ID

        self.consignmentIDs = consignmentIDs
        self.h_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.load_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.load_lim = [[-1 for _ in range(self.B)] for _ in range(self.L)]
        self.positions = {(0, 0)}
        self.packedItems = packedItems

        self.maxWt = maxWt
        self.vol = self.L * self.B * self.H

    def print_obj(self):
        print(self.L, self.B, self.H)

    def fit(self, l, b, h, stress_load):
        # finds a fit and returns
        loc = Location()
        posValid = True

        for p in self.positions:
            x = p[0]
            y = p[1]
            base = self.h_grid[x][y]

            if x + l > self.L or y + b > self.B or base + h > self.H:
                continue

            for m in range(l):
                for n in range(b):
                    if self.h_grid[x + m][y + n] != base:
                        posValid = False
                        break
                    elif self.load_lim[x + m][y + n] != -1 and self.load_lim[x + m][y + n] < stress_load:
                        posValid = False
                        break
                if posValid == False:
                    break

            if posValid:
                loc = Location(x, y, base)
                break

        if loc.x < 0:
            return Location()
        
        return loc

    def volOpt(self):
        pVol = 0
        for pack in self.packedItems:
            pVol += pack.vol

        return pVol/self.vol

    def outputRep(self):
        volOpt = self.volOpt
        op = "Volume Optimization {volOpt} Validitiy Check {check} Item Count {ic}".format(
            volOpt=self.volOpt(), check=self.checkValid(), ic=self.itemCount())
        print(op)
        return self.volOpt()

    def reset(self):
        self.positions.clear()
        self.positions = {(0, 0)}

        self.h_grid = [[0 for _ in range(self.B)] for _ in range(self.L)]

        self.packedItems.clear()

    def itemCount(self):
        return len(self.packedItems)

    def checkValid(self):
        for item in self.packedItems:
            if item.orientation == "H" and item.h != item.h1:
                return False
        return True
