import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
from plotting.base import read_config, set_style, apply_tweaks, tplot
from pathlib import Path

def main():
    config = read_config(sys.argv)
    print(config)
    set_style(config)


    # Generate some data to plot (or read it from a pre-generated file)
    x = np.linspace(0.1, 10.1, 500)
    yA = (x**2)*(np.sin(2*np.pi*x)**2 + 1.0)
    yB = (x**3)*(np.cos(2*np.pi*x)**2 + 1.0)

    # We will use the custom tplot() function which allows arbitrary
    # transformations of the x and y data to generate plots that are
    # log-log, lin-log, log-lin or anything else (e.g. a sinh axis is useful
    # for some of the RGBM plots).

    # First define the transformations that can be applied to each axis

    def tlin(x):
        return x

    def tlog(x):
        return np.log10(x)

    # Plot the data lin-lin
    fig, ax = plt.subplots(1,1)
    ax = tplot(x, yA, tlin, tlin, ax, yticks='lin', label = r"$x^2 (\sin^2(2 \pi x)+1)$")

    # Label axes
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')

    # Apply final tweaks and save figure as pdf
    fig, ax =  apply_tweaks(config, fig, ax)
    plt.savefig(Path(config["figures folder"]) / "lin-lin-example.pdf", bbox_inches='tight')
    plt.close()

    # Plot the data log-log
    fig, ax = plt.subplots(1,1)
    ax = tplot(x, yA, tlog, tlog, ax, xticks='log', yticks='log', label = r"$x^2 (\sin^2(2 \pi x)+1)$")
    ax = tplot(x, yB, tlog, tlog, ax, xticks='log', yticks='log', label = r"$x^3 (\cos^2(2 \pi x)+1)$")
    # By default there is no legend. To put it back:
    ax.legend()

    # Label axes
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')

    # Apply final tweaks and save figure as pdf
    fig, ax =  apply_tweaks(config, fig, ax)
    plt.savefig(Path(config["figures folder"]) / "log-log-example.pdf", bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
