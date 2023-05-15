import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.axes3d import Axes3D
import json
import random
import sys


def main():
    fname = sys.argv[1]
    f = open("output/{fname}.json".format(fname=fname), "r")
    l = json.load(f)

    X, Y, Z = l["Container"]
    x, y, z = np.indices((X, Y, Z))

    colors = np.empty([X, Y, Z] + [4], dtype=np.float32)
    alpha = .7

    voxels = None
    for item in l["Items"]:
        l = item['l']
        b = item['b']
        h = item['h']

        xl = item['position'][0]
        xu = xl + l
        yl = item['position'][1]
        yu = yl + b
        zl = item['position'][2]
        zu = zl + h

        cube = (x >= xl) & (x < xu) & (y >= yl) & (
            y < yu) & (z >= zl) & (z < zu)
        if voxels is None:
            voxels = cube
        else:
            voxels = voxels | cube
        colors[cube] = [random.random(), random.random(),
                        random.random(), alpha]

    # Plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Axis lim
    ax.axes.set_xlim3d(left=0, right=X)
    ax.axes.set_ylim3d(bottom=0, top=Y)
    ax.axes.set_zlim3d(bottom=0, top=Z)
    ax.axes.set_xlabel("X", labelpad=20)
    ax.axes.set_ylabel("Y", labelpad=20)
    ax.axes.set_zlabel("Z", labelpad=20)
    # Scaling
    x_scale = X
    y_scale = Y
    z_scale = Z

    scale = np.diag([x_scale, y_scale, z_scale, 1.0])
    scale = scale*(1.0/scale.max())
    scale[3, 3] = 1.0

    def short_proj():
        return np.dot(Axes3D.get_proj(ax), scale)

    ax.get_proj = short_proj

    # Final Plot
    ax.voxels(voxels, facecolors=colors)
    plt.show()


if __name__ == "__main__":
    main()
