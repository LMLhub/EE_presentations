"""
Generate figures for the example presentation using the shared plotting module.

Usage (from the presentation folder):
  cd presentations/example-presentation
  python generate-figs.py figure-config.yaml
"""

import sys
from pathlib import Path

# Add the repo root to sys.path so we can import shared.plotting
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

import matplotlib.pyplot as plt
import numpy as np
from shared.plotting import read_config, set_style, apply_tweaks


def main():
    config = read_config(sys.argv)
    print(config)
    set_style(config)

    figs_folder = Path(config["figures folder"])
    figs_folder.mkdir(parents=True, exist_ok=True)

    # ---- Figure 1: Sample Brownian motion paths with drift ----
    np.random.seed(42)
    n_steps = 500
    dt = 0.01
    t = np.linspace(0, n_steps * dt, n_steps)

    fig, ax = plt.subplots(1, 1)
    for mu, label, color in [
        (0.0, r"$\mu = 0$", "#004670"),
        (0.5, r"$\mu = 0.5$", "#e07000"),
        (1.0, r"$\mu = 1.0$", "#2a9d8f"),
    ]:
        increments = mu * dt + np.sqrt(dt) * np.random.randn(n_steps)
        path = np.cumsum(increments)
        ax.plot(t, path, label=label, color=color, lw=1.5)

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title("Brownian motion with drift")
    ax.legend()
    fig, ax = apply_tweaks(config, fig, ax)
    plt.savefig(figs_folder / "brownian-paths.pdf", bbox_inches="tight")
    plt.close()

    # ---- Figure 2: Ensemble of paths showing mean vs typical ----
    np.random.seed(123)
    n_paths = 50
    mu = 0.5
    sigma = 1.0

    fig, ax = plt.subplots(1, 1)
    all_paths = np.zeros((n_paths, n_steps))
    for i in range(n_paths):
        increments = mu * dt + sigma * np.sqrt(dt) * np.random.randn(n_steps)
        all_paths[i] = np.cumsum(increments)
        ax.plot(t, all_paths[i], color="#004670", alpha=0.15, lw=0.8)

    # Ensemble mean
    ensemble_mean = np.mean(all_paths, axis=0)
    ax.plot(t, ensemble_mean, color="#e07000", lw=2.5, label="Ensemble mean")
    ax.plot(t, mu * t, color="#2a9d8f", lw=2, ls="--", label=r"$\mu t$ (expected)")

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(rf"Ensemble of {n_paths} paths ($\mu={mu}$, $\sigma={sigma}$)")
    ax.legend()
    fig, ax = apply_tweaks(config, fig, ax)
    plt.savefig(figs_folder / "ensemble-paths.pdf", bbox_inches="tight")
    plt.close()

    print("Figures saved to", config["figures folder"])


if __name__ == "__main__":
    main()
