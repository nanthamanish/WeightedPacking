import os
import sys
import math
from helper import make_dir

WTPACK_PROBLEM_CNT = 100


def get_avg(outfname: str):
    f = open("output\\{}.txt".format(outfname), "r")
    vals = f.readlines()
    f.close()

    vals = [float(x.strip()) for x in vals]
    avg = sum(vals)/len(vals)

    sd = sum([pow(x - avg, 2) for x in vals])/len(vals)
    sd = math.sqrt(sd)

    print(round(avg, 3), round(sd, 3))

    return avg, sd


def main():
    fname = sys.argv[1]
    outfname = sys.argv[1]
    if len(sys.argv) > 2:
        outfname = sys.argv[2]

    make_dir(os.getcwd(), "output")
    delcmd = "del output\\{outfname}.txt".format(outfname=outfname)
    print(delcmd)
    os.system(delcmd)

    cmd = "py .\main.py {fname}_{num} {outfname}"
    for i in range(WTPACK_PROBLEM_CNT):
        print(cmd.format(fname=fname, outfname=outfname, num=i))
        os.system(cmd.format(fname=fname, outfname=outfname, num=i))

    get_avg(outfname)


if __name__ == "__main__":
    main()
