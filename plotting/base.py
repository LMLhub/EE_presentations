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
