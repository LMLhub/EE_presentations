"""
Slide deck definition for the example presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(str(Path(__file__).parent))
from figs.code.plots import plot_farmers_fable, plot_farmers_fable_individual


# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_brownian() -> None:
    """Interactive Brownian motion with adjustable drift and variance."""
    st.subheader("Brownian Motion with Drift")

    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider("Drift (μ)", -2.0, 2.0, 0.5, 0.1)
    with col2:
        sigma = st.slider("Volatility (σ)", 0.1, 3.0, 1.0, 0.1)
    with col3:
        n_paths = st.slider("Paths", 1, 50, 10, 1)

    n_steps = 500
    dt = 0.01
    t = np.linspace(0, n_steps * dt, n_steps)

    np.random.seed(42)

    fig, ax = plt.subplots(figsize=(9, 4))
    all_paths = np.zeros((n_paths, n_steps))
    for i in range(n_paths):
        increments = mu * dt + sigma * np.sqrt(dt) * np.random.randn(n_steps)
        all_paths[i] = np.cumsum(increments)
        ax.plot(t, all_paths[i], alpha=0.4, lw=0.8)

    # Ensemble mean
    if n_paths > 1:
        ensemble_mean = np.mean(all_paths, axis=0)
        ax.plot(t, ensemble_mean, color="black", lw=2.5, label="Ensemble mean")

    # Theoretical expectation
    ax.plot(t, mu * t, color="red", lw=2, ls="--", label=rf"$\mu t = {mu:.1f}\,t$")

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(rf"$dx = {mu:.1f}\,dt + {sigma:.1f}\,dW$")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_farmers_fable() -> None:
    """Interactive Farmer's Fable simulation."""
    st.subheader("Farmer's Fable Simulation")

    col1, col2, col3 = st.columns(3)
    with col1:
        g = st.slider("Growth factor (g)", 0.1, 3.0, 1.0, 0.1)
    with col2:
        r = st.slider("Risk factor (r)", 0.0, 3.0, 0.5, 0.1)
    with col3:
        n_paths = st.slider("Paths", 1, 50, 10, 1)

    n_steps = 1000
    t = np.linspace(0, n_steps , n_steps)

    np.random.seed(42)

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(9, 4))
    fig, ax1 = plot_farmers_fable_individual(g, r, n_paths, n_steps, fig, ax1)
    fig, ax2 = plot_farmers_fable(g, r, n_paths, n_steps, fig, ax2)
    st.pyplot(fig)
    plt.close(fig)

APP_SLIDES: dict = {
    "brownian": app_slide_brownian,
    "farmers_fable": app_slide_farmers_fable,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
    ("pdf", 0),             # title page
    ("pdf", 1),             # Brownian motion with drift figure
    ("pdf", 2),             # ensemble averages figure
    ("pdf", 3),             # key observations
    ("app", "brownian"),    # interactive Brownian motion
    ("app", "farmers_fable"), # interactive Farmer's Fable
    ("pdf", 4),             # thank you
]
