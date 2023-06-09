from helper import read_floats, read_ints, to_str
from functools import cmp_to_key
from package import Package, cmp_pack
from container import Container
from packer import Packer
import sys
import time
import json

PACK_SIZE_LIM = 300


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

    print("CPU Mode - Numpy")

    fname = sys.argv[1]
    inf = "input/{f}.txt".format(f=fname)

    c, packages = get_input_from_file(inf)

    packages.sort(key=cmp_to_key(cmp_pack))

    tot_vol = 0
    for pack in packages:
        tot_vol += pack.vol

    if len(packages) > PACK_SIZE_LIM:
        print("Skipping, Package count high")
        outfname = sys.argv[2]
        outf = "output/{f}.txt".format(f=outfname)
        outf = open(outf, "a")
        outf.write("{r} {ic}\n".format(r=0, ic=0))
        outf.close()

        timef = open("output/time_{f}.txt".format(f=outfname), "a")
        timef.write("{r}\n".format(r=0))
        return

    print("Maximum Utilization: {mu}".format(mu=tot_vol/c.vol))

    # packing
    start = time.time()
    P = Packer(packages=packages, containers=[c])
    packed_c = P.three_d_pack(C=c, items=packages)
    packed_c.output_rep()
    end = time.time()

    # writing to file
    outfname = sys.argv[2]
    outf = "output/{f}.txt".format(f=outfname)
    outf = open(outf, "a")
    outf.write("{r} {ic}\n".format(
        r=packed_c.vol_opt(), ic=packed_c.item_count()))
    outf.close()

    timef = open("output/time_{f}.txt".format(f=outfname), "a")
    timef.write("{r}\n".format(r=end-start))

    print(end-start)

    # writing packing to json file
    ljson = {}
    ljson["Container"] = [c.L, c.B, c.H]
    item_json = []
    for I in packed_c.packed_items:
        i = {}
        i["position"] = [I.pos.x, I.pos.y, I.pos.z]
        i["l"] = I.l1
        i["b"] = I.b1
        i["h"] = I.h1
        item_json.append(i)
    ljson["Items"] = item_json
    final = json.dumps(ljson, indent=4)

    json_str = json.dumps(ljson, indent=4)
    with open('output/{f}.json'.format(f=outfname), 'w') as fout:
        fout.write(json_str)


if __name__ == "__main__":
    main()
