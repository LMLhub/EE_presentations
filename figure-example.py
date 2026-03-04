import matplotlib.pyplot as plt
import numpy as np
import pickle
import sys
from plotting.base import read_config, set_style, apply_tweaks

def main():
    config = read_config(sys.argv)
    set_style(config)

    # Example data: a simple sine wave
    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label='Sine Wave')
    ax.set_xlabel('x')
    ax.set_ylabel('sin(x)')
    ax.set_title('Example Figure')
    ax.legend()
    ax.grid(True)

    fig, ax = apply_tweaks(config, fig, ax)
    plt.show()

if __name__ == "__main__":
    main()
