import random
from helper import read_floats, read_ints, rand_range, to_str

DENSITY_LOWER_BOUND = 0.5
DENSITY_UPPER_BOUND = 10
DESTINATIONS = 100
PRECISION = 3


def main():
    random.seed()
    inp = input("Enter File Name (without extension): ")
    fname = "wtpack/{}.txt".format(inp)
    print(fname)
    f_in = open(fname, "r")

    for p in range(100):
        cont_dim = read_ints(f_in)
        n_packs, vol = read_floats(f_in)
        n_packs = int(n_packs)
        t_boxes = 0
        out_fname = "input/{inp}_{prob}.txt".format(inp=inp, prob=p)
        f_out = open(out_fname, "w")

        id = 0
        items = []
        for i in range(n_packs):
            l, lo, b, bo, h, ho, numBox, wt, lbear, bbear, hbear = read_floats(
                f_in)

            l, lo, b, bo, h, ho, numBox = [
                int(x) for x in [l, lo, b, bo, h, ho, numBox]]

            t_boxes += numBox

            density = rand_range(DENSITY_LOWER_BOUND, DENSITY_UPPER_BOUND)

            wt = round(wt * density, PRECISION)
            lbear = round(wt * lbear, PRECISION)
            bbear = round(wt * bbear, PRECISION)
            hbear = round(wt * hbear, PRECISION)
            for j in range(numBox):
                dest = random.randint(1, DESTINATIONS)
                item = [id, dest, l, lo, b, bo, h, ho, wt, lbear, bbear, hbear]
                items.append(item)
                id += 1

        first_line = cont_dim
        first_line.append(t_boxes)
        contStr = to_str(first_line)

        f_out.write(contStr)
        for item in items:
            out_str = to_str(item)
            f_out.write(out_str)
        f_out.close()
    f_in.close()


if __name__ == "__main__":
    main()
