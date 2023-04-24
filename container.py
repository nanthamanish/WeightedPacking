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
        self.v = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.minH = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.positions = {(0, 0)}
        self.packedItems = packedItems

        self.maxWt = maxWt
        self.vol = self.L * self.B * self.H

    def printObj(self):
        print(self.L, self.B, self.H)

    def fit(self, l, b, h):
        loc = Location()
        posValid = True

        for p in self.positions:
            x = p[0]
            y = p[1]
            base = self.v[x][y]

            if x + l > self.L or y + b > self.B or base + h > self.H:
                continue

            for m in range(l):
                for n in range(b):
                    if self.v[x + m][y + n] != base or self.minH[x + m][y + n] >= h:
                        posValid = False
                        break
                if posValid == False:
                    break

            if posValid:
                loc = Location(x, y, base)
                break

        if loc.x < 0:
            return Location()

        for m in range(loc.x, loc.x + l):
            for n in range(loc.y, loc.y + b):
                if self.v[m][n] >= self.v[loc.x][n]:
                    break
                self.minH[m][n] = self.v[loc.x][n] = self.v[m][n]

        if loc.x + l < self.L:
            self.positions.add((loc.x + l, loc.y))

        if loc.y + b < self.B:
            self.positions.add((loc.x, loc.y + b))
        
        return loc
    
    def volOpt(self):
        pVol = 0
        for pack in self.packedItems:
            pVol += pack.pVol

        return pVol/self.vol

    def outputRep(self, i):
        volOpt = self.volOpt
        op = "{i}: Volume Optimization {volOpt} Validitiy Check {check} Item Count {ic}".format(
            i=i, volOpt=volOpt, check=self.checkValid(), ic=self.itemCount())
        print(op)
        return volOpt

    def reset(self):
        self.positions.clear()
        self.positions = {(0, 0)}

        self.v = [[0 for _ in range(self.B)] for _ in range(self.L)]
        self.minH = [[0 for _ in range(self.B)] for _ in range(self.L)]

        self.packedItems.clear()

    def itemCount(self):
        return len(self.packedItems)

    def checkValid(self):
        for item in self.packedItems:
            if item.orientation == "H" and item.h != item.h1:
                return False
        return True
