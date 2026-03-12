import numpy as np
import pandas as pd
import os
import yaml
import matplotlib
import matplotlib.pyplot as plt

def read_config(argv):
    # Determine the name of the config file to be used
    filename='config_default.yaml'
    if len(argv) == 1:
        print("No config file specified. Assuming config_default.yaml")
    else:
        filename = argv[1]
        print("Using config file ", filename)

    # Check that the config file exists and is readable
    if not os.access(filename, os.R_OK):
        print("Config file ", filename, " does not exist or is not readable. Exiting.")
        exit()

    # Read the config file
    f = open(filename,'r')
    config = yaml.load(f, Loader=yaml.SafeLoader)
    f.close()

    return config

def set_style(config):
    matplotlib.rc('image', cmap='gray')
    matplotlib.style.use('seaborn-v0_8-colorblind')
    #matplotlib.style.use('classic')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.weight'] = 'normal'
    plt.rcParams['font.size'] = 12

    xdim = config['figure size']['x']
    ydim = config['figure size']['y']
    plt.rcParams['figure.figsize'] = (xdim, ydim)

    return

def apply_tweaks(config, fig, ax):
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    # Set the display aspect ratio
    ratio = config['aspect ratio']
    #xleft, xright = ax.get_xlim()
    #ybottom, ytop = ax.get_ylim()
    #ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    size = fig.get_size_inches()[1]
    fig.set_size_inches(size/ratio, size)
    return fig, ax


def calculate_axis_ticks(ax, cz, mode='log', axis='y'):
    if axis == 'y':
        minval, maxval = ax.get_ylim()
        ticks = ax.get_yticks()
        minor_ticks = ax.get_yticks(minor=True)
        ticklabels = ax.get_yticklabels()
    elif axis == 'x':
        minval, maxval = ax.get_xlim()
        ticks = ax.get_xticks()
        minor_ticks = ax.get_xticks(minor=True)
        ticklabels = ax.get_xticklabels()
    else:
         print("calculate_axis_ticks(): axis must be x or y")
         exit()

    #print([mode, axis])
    eps = 0.1*(maxval-minval)
    if mode == 'log':
        # This is for a log scale
        data_range = int(round(maxval-minval))
        step = max([1,int((data_range - (data_range%6))/6)])
        ticks = [ int(round(v)) for v in np.arange(minval, maxval+eps, step)]
        # If rounding results in ticks not spanning the data range, add extra ticks
        if ticks[0] > minval:
            ticks.insert(0,ticks[0]-step)
        if ticks[-1] < maxval:
            ticks.append(ticks[-1]+step)
        # Generate the labels as strings
        ticklabels = [r"$10^{{{0}}}$".format(tick) for tick in ticks]
        # Replace 10^0 and 10^1 by 1 and 10 respectively
        ticklabels = [label.replace('10^{0}', '1') for label in ticklabels]
        ticklabels = [label.replace('10^{1}', '10') for label in ticklabels]
        # Now generate the minor ticks
        minor_ticks = []
        for i in range(min(ticks), max(ticks)):
            for j in range(2,10):
                minor_ticks.append(i+np.log10(j))

    elif mode == 'linear':
        # This is for a linear scale
        # print("calculate_axis_ticks(): mode = 'linear' mode not implemented yet!")
        # Use existing tick since it's usually OK for linear!
        pass
    elif mode == 'uniform':
        # This is for uniformly spaced ticks on arbitrarily transformed axis
        print("calculate_axis_ticks(): mode = 'uniform' not implemented yet!")
    else:
        print("calculate_axis_ticks(): Error - unknown mode, ", mode)

    return ticks, ticklabels, minor_ticks


def tplot(x, y, cx, cy, ax, label=None, xticks='linear', yticks='log', minorticks=True, **kwargs):
    # Transform the data and add it to the axis
    xt = list(map(cx, x))
    yt = list(map(cy, y))
    ax.plot(xt, yt, label=label, **kwargs)

    # Set the ticks for the y axis
    ticks, ticklabels, minor_ticks = calculate_axis_ticks(ax, cy, mode=yticks, axis='y')
    ax.set_yticks(ticks)
    ax.set_yticklabels(ticklabels)
    if minorticks:
        ax.set_yticks(minor_ticks, minor = True)

    # Set the ticks for the x axis
    ticks, ticklabels, minor_ticks = calculate_axis_ticks(ax, cx, mode=xticks, axis='x')
    ax.set_xticks(ticks)
    ax.set_xticklabels(ticklabels)
    if minorticks:
        ax.set_xticks(minor_ticks, minor = True)
    return ax
