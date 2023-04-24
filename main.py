from package import Package
from container import Container
from helper import read_floats, read_ints, rand_range, to_str
from functools import cmp_to_key


def cmp_pack(pa: Package, pb: Package):
    if pa.dest == pb.dest:
        if pa.maxDim < pb.maxDim:
            return 1
        elif pa.maxDim > pb.maxDim: 
            return -1
        else:
            return 0
    
    elif pa.dest < pb.dest:
        return 1
    else:
        return -1


def get_input_from_file(fname) -> tuple[Container, list[Package]]:
    f_in = open(fname, "r")
    c_l, c_b, c_h, numPack = read_ints(f_in)
    c = Container(x=c_l, y=c_b, z=c_h)

    packages = []
    for i in range(numPack):
        id, dest, l, lo, b, bo, h, ho, wt, lbear, bbear, hbear = read_floats(
            f_in)
        id, dest, l, lo, b, bo, h, ho = [
            int(x) for x in [id, dest, l, lo, b, bo, h, ho]]
        p = Package(ID=id, wt=wt, dest=dest,
                    l=l, b=b, h=h,
                    stackLoad=[lbear, bbear, hbear],
                    stackable=True,
                    orientation=[lo, bo, ho])
        packages.append(p)
    return c, packages


def main():
    fname = input("Enter File Name (without Extension): ")
    fname = "input/{f}.txt".format(f=fname)

    c, packages = get_input_from_file(fname)
    # c.printObj()

    packages.sort(key=cmp_to_key(cmp_pack))

    # for pack in packages:
    #     pack.print_obj()


if __name__ == "__main__":
    main()
