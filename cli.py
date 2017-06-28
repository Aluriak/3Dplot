"""Plot 3D graph.

usage:
    cli.py <inputcsv> <xcol> <ycol> <zcol>...  --xlab=LABEL --ylab=LABEL --zlab=LABEL,... --select=STRING

"""

import plot3d

def cli() -> dict:
    import argparse
    parser = argparse.ArgumentParser("Plot 3D graphs")
    parser.add_argument('inputcsv', type=str, help="the input CSV file")
    parser.add_argument('xcol', type=str, help="name of the col to use as x dimension")
    parser.add_argument('ycol', type=str, help="name of the col to use as y dimension")
    parser.add_argument('zcol', type=str, metavar='zcolumns', nargs='+', help="name(s) of the col to use as z dimension")
    parser.add_argument('--xlab', type=str, help="label to use for the x dimension", default=None)
    parser.add_argument('--ylab', type=str, help="label to use for the y dimension", default=None)
    parser.add_argument('--zlab', type=str, metavar='zlabels', nargs='+', help="label(s) to use for the z dimension", default=None)
    parser.add_argument('--select', type=str, nargs='+', help="colname=value restrict the data to rows meeting the condition", default={})
    return parser.parse_args()

if __name__ == "__main__":
    args = cli()
    xlabel = args.xlab or args.xcol
    ylabel = args.ylab or args.ycol
    zlabels = args.zlab or args.zcol

    selection = {}
    for select in args.select:
        colname, colvalue = select.split('=')
        selection[colname] = colvalue

    xs, ys, zss = plot3d.make_data(args.inputcsv, args.xcol, args.ycol, args.zcol, restrict_to=selection)
    print(xs, ys, zss)
    plot3d.plot_multiple_z(xs, ys, zss, xlabel, ylabel, zlabels)

