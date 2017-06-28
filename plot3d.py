"""Plot 3D graph.

See cli.py for CLI around these.

"""

import itertools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


COLORS = itertools.cycle([cm.plasma, cm.rainbow])


def plot_z(xs, ys, zs, xlabel, ylabel, zlabel, color=next(iter(COLORS))):
    """wrapper around plot function, for only one z to plot"""
    return plot_multiple_z(xs, ys, [zs], xlabel, ylabel, [zlabel], colors=[color])


def plot_multiple_z(xs, ys, zss, xlabel, ylabel, zlabels, colors=COLORS):
    # fig = plt.figure()

    # Plot the surface.

    for zs, cmap, zlabel in zip(zss, colors, zlabels):
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        surf = ax.plot_surface(xs, ys, zs, cmap=cmap,
                               linewidth=10, antialiased=True,
                               vmin=zs.min(), vmax=zs.max())

        # Customize the z axis.
        ax.set_zlim(zs.min(), zs.max())
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_zlabel(zlabel)

        # Add a color bar which maps values to colors.
        # plt.pcolor(xs, ys, zs, vmin=0.2)
        fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


# Make data.
import csv
from collections import defaultdict


def isfloat(value:str) -> float:
  try:
    float(value)
    return True
  except ValueError:
    return False


def converted_value(val:str) -> int or float or str:
    if val.isnumeric():
        return int(val)
    if isfloat(val):
        return float(val)
    return str(val)  # not int nor float


def make_data(csvfile:str, xcol:str, ycol:str, zcols:str, restrict_to:dict={}) -> np.array:
    """Read given csvfile, and return corresponding numpy array ready
    to be plotted for each given z column.

    Retained columns are only the ones given as *col parameters.
    Multiple zcols are expected.

    csvfile -- input file formatted in csv containing all given column names
    xcol -- name of the column in the file to use in x.
    xtype -- cast values in column x with given callable
    restrict_to -- map of column to value. Only rows with column value
                   set to given one are kept.

    """
    data = defaultdict(dict)  # {x: {y: {zcol: zval}}}
    with open(csvfile) as ifd:
        reader = csv.DictReader(ifd)
        for nol, line in enumerate(reader, start=1):
            add = not restrict_to
            if restrict_to:
                for colname, colvalue in restrict_to.items():
                    print(converted_value(line[colname]),  colvalue)
                    if converted_value(line[colname]) == colvalue:
                        add = True
            if add:
                zdata = {zcol: converted_value(line[zcol]) for zcol in zcols}
                data[converted_value(line[xcol])][converted_value(line[ycol])] = zdata
    # form the X and Y axis correctly
    xdata = sorted(data.keys())
    ydata = sorted(tuple(next(iter(data.values()))))
    xdata, ydata = np.meshgrid(xdata, ydata)
    zdatas = []
    # form the Z axis for each of them
    for zcol in zcols:
        table_z = []
        # form the z axis
        for dim_x, dim_y in zip(xdata, ydata):
            table_z.append([])
            for x, y in zip(dim_x, dim_y):
                table_z[-1].append(data[x][y][zcol])
        zdatas.append(np.array(table_z))
    return xdata, ydata, zdatas
