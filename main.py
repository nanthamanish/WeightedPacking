from helper import read_floats, read_ints, to_str
from functools import cmp_to_key
from package import Package, cmp_pack
from container import Container
from packer import Packer
import sys


def get_input_from_file(fname) -> tuple[Container, list[Package]]:
    f_in = open(fname, "r")
    c_l, c_b, c_h, numPack = read_ints(f_in)
    c = Container(x=c_l, y=c_b, z=c_h)

    packages = []
    for i in range(numPack):
        id, dest, wt, l, b, h, lo, bo, ho, lbear, bbear, hbear = read_floats(
            f_in)
        id, dest, l, lo, b, bo, h, ho = [
            int(x) for x in [id, dest, l, lo, b, bo, h, ho]]
        p = Package(ID=id, wt=wt, dest=dest,
                    l=l, b=b, h=h,
                    stack_load=[lbear, bbear, hbear],
                    stackable=True,
                    orientation=[lo, bo, ho])
        packages.append(p)
    return c, packages


def main():
    #fname = input("Enter File Name (without Extension): ")
    fname = sys.argv[1]
    fname = "input/{f}.txt".format(f=fname)

    c, packages = get_input_from_file(fname)

    packages.sort(key=cmp_to_key(cmp_pack))

    tot_vol = 0

    for pack in packages:
        tot_vol += pack.vol
        # print(pack.dest, max([pack.orientation[i] * pack.stack_load[i] for i in range(3)]))
        # pack.print_obj()

    print(tot_vol/c.vol)

    P = Packer(packages=packages, containers=[c])
    res = P.pack()
    print(res)


if __name__ == "__main__":
    main()
