"""
Slide deck definition for the example presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text



# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_leverage() -> None:
    """Interactive illustration of the role of leverage for a 
    portfolio return. Adjustable parameters: riskfree rate, drift and variance of stock."""
    color_red = plt.rcParams['axes.prop_cycle'].by_key()['color'][3]
    color_green = plt.rcParams['axes.prop_cycle'].by_key()['color'][2]
    color_blue = plt.rcParams['axes.prop_cycle'].by_key()['color'][0]
    color_yellow = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]
    color_grey = plt.rcParams['axes.prop_cycle'].by_key()['color'][7]
    
    st.subheader("Optimal leverage")

    col1, col2 = st.columns([2, 6])

    with col1:
        st.markdown("Leverage")
        leverage = st.slider("Leverage (l)", -1.0, 3.0, 0.2, 0.1)
        st.markdown("Risky asset")
        mu_s = st.slider("Drift (μ_s)", -0.10, 0.30, 0.20, 0.01)
        sigma_s = st.slider("Volatility (σ_s)", 0.0, 1.0, 0.4, 0.01)
        st.markdown("Safe asset")
        mu_r = st.slider("Drift (μ_r)", -0.10, 0.30, 0.03, 0.01)
    
    n_steps = 500
    dt = 0.1
    t = np.linspace(0, n_steps * dt, n_steps)

    np.random.seed(42)

    fig, ax = plt.subplots(1,2,figsize=(9, 3.6))
    path = np.zeros(n_steps)
    
    # Generate standard normal incrementsf
    Z = np.random.randn(n_steps)
    
    # Geometric Brownian Motion increments
    S0 = 100
    path[0] = S0
    for j in range(1, n_steps):
        mu_e = mu_s - mu_r #excess return
        path[j] = path[j-1] * np.exp((mu_r + leverage * mu_e - leverage**2 * 0.5 * sigma_s**2) * dt + leverage * sigma_s * np.sqrt(dt) * Z[j])
    
    #Panel 1
    ax[0].plot(t, path, color=color_blue, label = rf"Trajectory, $l = {leverage}$", alpha=1, lw=0.8)
    
    # Theoretical expectation
    # ax.plot(t, S0*np.exp((mu_r + leverage * mu_e)*t), color= color_red, lw=2, ls="-", label="Expectation value")

    # Theoretical time average
    growth_rate = mu_r + leverage * mu_e - leverage**2 * 0.5 * sigma_s**2
    ax[0].plot(t, S0*np.exp(growth_rate * t), color=color_green, lw=2, ls="-", label=rf"Exponential growth at time average growth rate, $l = {leverage}$")

    # Theoretical maximum time average
    lev_opt = mu_e / sigma_s**2
    ax[0].plot(t, S0*np.exp((mu_r + lev_opt * mu_e - lev_opt**2 * 0.5 * sigma_s**2) * t), color=color_grey, lw=0.8, ls="--", label=rf"Exponential growth at optimal time average growth rate, $l = {lev_opt:.2f}$")

    ax[0].set_xlabel("Time, $t$")
    ax[0].set_ylabel("$x(t)$")
    #ax.set_title(rf"$dx = x({mu:.2f}\,dt + {sigma:.2f}\,dW$)")
    ax[0].set_yscale('log')
    #ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.2) )
    ax[0].grid(False)
    
    #Plot 2
    n = 500
    l_linspace = np.linspace(-1, 3,n)
    tagr = np.zeros(n)
    for i in range(n):
        tagr[i] = mu_r + l_linspace[i] * mu_e - l_linspace[i]**2 * 0.5 * sigma_s**2
    
    # Plot relationship between leverage and growth rate
    ax[1].axhline(0, linestyle=':', color = "black",  linewidth=1)
    ax[1].plot(l_linspace, tagr, color = color_grey, label = "Time average growth rate" )

    ax[1].scatter(leverage, growth_rate, color = color_blue )
    
    texts = [ax[1].text(leverage, growth_rate, rf"$l={leverage}, g = {growth_rate:.2f}$", color=color_blue, ha="center")]
    adjust_text(
        texts,
        only_move={'points':'y', 'text':'xy'},
        expand_points=(1.1,1.1),
        expand_objects=(1.0,1.0)
    )
    #ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.2) )
    ax[1].set_xlabel("Leverage, $l$")
    ax[1].set_ylabel("Growth rate, $g$")
    
    # Collect all handles and labels from both axes
    handles, labels = [], []
    for ax in [ax[0], ax[1]]:
        h, l = ax.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)

    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=1)

    fig.subplots_adjust(wspace=0.3)
    
    with col2:
        st.pyplot(fig)
    
    plt.close(fig)

APP_SLIDES: dict = {
    "leverage": app_slide_leverage,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
    #("pdf", 0),             # title page
    #("pdf", 1),             # Brownian motion with drift figure
    #("pdf", 2),             # ensemble averages figure
    #("pdf", 3),             # key observations
    ("app", "leverage"),    # interactive Brownian motion
    ("pdf", 4),             # thank you
]