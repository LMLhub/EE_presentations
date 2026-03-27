"""
Slide deck definition for the example presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt



# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_trajectories() -> None:
    """Example trajectories."""
    st.markdown("""
        <style>
            .slide-title {
                color: rgb(0, 70, 112);
                font-size: 2rem !important;
                font-weight: 400;
                font-family: sans-serif !important;
                margin-bottom: 3.5rem;
                margin-top: 2.5rem;   
            }
        </style>
    """, unsafe_allow_html=True)

    color_red = plt.rcParams['axes.prop_cycle'].by_key()['color'][3]
    color_green = plt.rcParams['axes.prop_cycle'].by_key()['color'][2]
    color_blue = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
    color_yellow = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]
    color_grey = plt.rcParams['axes.prop_cycle'].by_key()['color'][7]

    st.set_page_config(layout="centered")
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<p class="slide-title">Finite ensemble of GBM trajectories</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider(rf"Drift ($\mu$)", -0.1, 0.5, 0.05, 0.01)
    with col2:
        sigma = st.slider(rf"Volatility ($\sigma$)", 0.0, 2.0, 0.4, 0.01)
    with col3:
        n_paths = st.slider("Population ($N$)", 1, 50, 1, 7)

    n_steps = 500
    dt = 1
    t = np.linspace(0, n_steps * dt, n_steps)

    np.random.seed(1)
    
    fig, ax = plt.subplots(figsize=(9, 4))
    all_paths = np.zeros((n_paths, n_steps))
    S0 = 1
    
    for i in range(n_paths):
        # Generate standard normal increments
        Z = np.random.randn(n_steps)
        # Geometric Brownian Motion increments
        all_paths[i, 0] = S0
        for j in range(1, n_steps):
            all_paths[i, j] = all_paths[i, j-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[j])
        ax.plot(t, all_paths[i], color=color_grey, alpha=0.4, lw=0.8)

    # Theoretical time average
    ax.plot(t, np.exp((mu-  0.5 * sigma**2)* t), color=color_green, lw=2, ls="-", label="Time average")

    # Theoretical expectation
    ax.plot(t, np.exp(mu * t), color= color_red, lw=2, ls="-", label="Expectation value")

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(rf"$dx = x({mu:.2f}\,dt + {sigma:.2f}\,dW$)")
    ax.set_yscale('log')
    ax.set_xlim(0,500)

    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    #ax.legend(loc="upper left")
    ax.grid(False)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_inequality() -> None:
    """Figure 8.5, with adjustable population size drift and variance."""
    st.markdown("""
        <style>
            .slide-title {
                color: rgb(0, 70, 112);
                font-size: 2rem !important;
                font-weight: 400;
                font-family: sans-serif !important;
                margin-bottom: 3.5rem;
                margin-top: 2.5rem;   
            }
        </style>
    """, unsafe_allow_html=True)

    color_red = plt.rcParams['axes.prop_cycle'].by_key()['color'][3]
    color_green = plt.rcParams['axes.prop_cycle'].by_key()['color'][2]
    color_blue = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
    color_yellow = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]
    color_grey = plt.rcParams['axes.prop_cycle'].by_key()['color'][7]

    st.set_page_config(layout="centered")
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<p class="slide-title">Finite ensemble of GBM trajectories</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider(rf"Drift ($\mu$)", -0.1, 0.5, 0.05, 0.01)
    with col2:
        sigma = st.slider(rf"Volatility ($\sigma$)", 0.0, 2.0, 0.4, 0.01)
    with col3:
        n_paths = st.slider("Population ($N$)", 1, 500, 100, 10)

    n_steps = 500
    dt = 1
    t = np.linspace(0, n_steps * dt, n_steps)

    np.random.seed(1)
    
    fig, ax = plt.subplots(figsize=(9, 4))
    all_paths = np.zeros((n_paths, n_steps))
    S0 = 1
    
    for i in range(n_paths):
        # Generate standard normal increments
        Z = np.random.randn(n_steps)
        # Geometric Brownian Motion increments
        all_paths[i, 0] = S0
        for j in range(1, n_steps):
            all_paths[i, j] = all_paths[i, j-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z[j])
        ax.plot(t, all_paths[i], color=color_grey, alpha=0.4, lw=0.8)

    # Theoretical time average
    ax.plot(t, np.exp((mu-  0.5 * sigma**2)* t), color=color_green, lw=2, ls="-", label="Time average")

    # Theoretical expectation
    ax.plot(t, np.exp(mu * t), color= color_red, lw=2, ls="-", label="Expectation value")

    # Ensemble mean
    if n_paths > 1:
        ensemble_mean = np.mean(all_paths, axis=0)
        ax.plot(t, ensemble_mean, color=color_blue, lw=2.5, label="Population mean")

    # Maximum value contribution
    ax.plot(t, 1/n_paths*np.max(all_paths, axis=0), color=color_yellow, lw=0.8, ls="-", label="Contribution of max")

    
    # Critical time
    t_c = 2*np.log(n_paths)/sigma**2
    ax.axvline(t_c, color="black", lw=1, ls=":", label="Critical time")

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(rf"$dx = x({mu:.2f}\,dt + {sigma:.2f}\,dW$)")
    ax.set_yscale('log')
    ax.set_xlim(0,500)

    ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
    #ax.legend(loc="upper left")
    ax.grid(False)
    st.pyplot(fig)
    plt.close(fig)


APP_SLIDES: dict = {
    "traj": app_slide_trajectories,
    "ineq": app_slide_inequality,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
   ("pdf", 0),              # title page
   ("pdf", 1),              # table of contents
   ("pdf", 2),              # narrative arc
   ("pdf", 3),              # GBM
   ("app", "traj"),         # interactive trajectories
   ("app", "ineq"),         # interactive Brownian motion
   ("pdf", 4),              # thank you
]
