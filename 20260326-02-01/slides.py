"""
Slide deck definition for the example presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

COLORS = {
    "red":            plt.rcParams['axes.prop_cycle'].by_key()['color'][3],
    "green":          plt.rcParams['axes.prop_cycle'].by_key()['color'][2],
    "blue":           plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    "yellow":         plt.rcParams['axes.prop_cycle'].by_key()['color'][1],
    "grey":           plt.rcParams['axes.prop_cycle'].by_key()['color'][7],
    # colors for markowitz
    "efficient_frontier":   plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    "inefficient_frontier": plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
    "cal":                  "black",
    "assets":               plt.rcParams['axes.prop_cycle'].by_key()['color'][7],
    "tangency":             plt.rcParams['axes.prop_cycle'].by_key()['color'][3],
    "risk_free":            "black",
}    

# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_leverage() -> None:
    """Interactive illustration of the role of leverage for a 
    portfolio return. Adjustable parameters: riskfree rate, drift and variance of stock."""
    st.markdown("""
        <style>
            .slide-title {
                color: rgb(0, 70, 112);
                font-size: 2rem !important;
                font-weight: 400;
                font-family: sans-serif;
                margin-bottom: 3.5rem !important;
            }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="slide-title">Optimal leverage</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 6])

    with col1:
        st.markdown("")
        leverage = st.slider(rf"Leverage, $\ell$", 0.0, 3.0, 0.2, 0.1)
        mu_s = st.slider("Risky asset - drift, $\mu_s$", -0.10, 0.30, 0.20, 0.01)
        sigma_s = st.slider("Risky asset - volatility, $\sigma_s$", 0.0, 1.0, 0.4, 0.01)
        mu_r = st.slider("Risk-free asset - drift, $\mu_r$", -0.10, 0.30, 0.03, 0.01)
    
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
    ax[0].plot(t, path, color=COLORS["blue"], label = rf"Trajectory, $\ell = {leverage}$", alpha=1, lw=0.8)
    
    # Theoretical expectation
    # ax.plot(t, S0*np.exp((mu_r + leverage * mu_e)*t), color= COLORS["red"], lw=2, ls="-", label="Expectation value")

    # Theoretical time average
    growth_rate = mu_r + leverage * mu_e - leverage**2 * 0.5 * sigma_s**2
    ax[0].plot(t, S0*np.exp(growth_rate * t), color=COLORS["green"], lw=2, ls="-", label=rf"Exponential growth at time average growth rate, $\ell = {leverage}$")

    # Theoretical maximum time average
    lev_opt = mu_e / sigma_s**2
    ax[0].plot(t, S0*np.exp((mu_r + lev_opt * mu_e - lev_opt**2 * 0.5 * sigma_s**2) * t), color=COLORS["grey"], lw=0.8, ls="--", label=rf"Exponential growth at optimal time average growth rate, $\ell = {lev_opt:.2f}$")

    ax[0].set_xlabel("Time, $t$")
    ax[0].set_ylabel("$x(t)$")
    #ax.set_title(rf"$dx = x({mu:.2f}\,dt + {sigma:.2f}\,dW$)")
    ax[0].set_yscale('log')
    #ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, -0.2) )
    ax[0].grid(False)
    
    #Plot 2
    n = 500
    l_linspace = np.linspace(0, 3,n)
    tagr = np.zeros(n)
    for i in range(n):
        tagr[i] = mu_r + l_linspace[i] * mu_e - l_linspace[i]**2 * 0.5 * sigma_s**2
    
    # Plot relationship between leverage and growth rate
    ax[1].axhline(0, linestyle=':', color = "black",  linewidth=1)
    ax[1].plot(l_linspace, tagr, color = COLORS["grey"], label = "Time average growth rate" )

    ax[1].scatter(leverage, growth_rate, color = COLORS["blue"] )
    
    texts = [ax[1].text(leverage, growth_rate, rf"$\ell={leverage}, \bar g = {growth_rate:.2f}$", color=COLORS["blue"], ha="center")]
    adjust_text(
        texts,
        only_move={'points':'y', 'text':'xy'},
        expand_points=(1.1,1.1),
        expand_objects=(1.0,1.0)
    )
    #ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, -0.2) )
    ax[1].set_xlabel("Leverage, $\ell$")
    ax[1].set_ylabel(rf"Growth rate, $\bar g$")
    
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


def app_slide_markowitz():
    st.markdown("""
        <style>
            .slide-title {
                color: rgb(0, 70, 112);
                font-size: 2rem !important;
                font-weight: 400;
                font-family: sans-serif;
                margin-bottom: 3.5rem !important;
            }
            .subheader {
                color: rgb(0, 70, 112);
                font-size: 1rem !important;
                font-weight: 600;
                font-family: sans-serif;
                margin-bottom: 1.5rem !important;
                margin-top: 1.5rem !important;
            }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="slide-title">Portfolio choice theory</p>', unsafe_allow_html=True)

    markdown1 = "Choose ANY combination of the tangency portfolio and the risk-free asset."
    markdown2 = "Choose the growth-rate optimal portfolio."
    
    # Preparing for not having two contours at the same time.
    if "show_sharpe" not in st.session_state:
        st.session_state.show_sharpe = False
    if "show_growth_rate" not in st.session_state:
        st.session_state.show_growth_rate = False

    def on_sharpe():
        if st.session_state.show_sharpe:
            st.session_state.show_growth_rate = False

    def on_growth():
        if st.session_state.show_growth_rate:
            st.session_state.show_sharpe = False

    col1, col2 = st.columns([2, 6])

    # --- Sidebar controls ---
    with col1:
        show_frontier = st.toggle("Efficient frontier", value=False)
        show_riskfree = st.toggle("Risk-free asset", value=False)
        show_CML = st.toggle("Capital Market Line", value=False)
        show_sharpe      = st.toggle("Sharpe ratio contour",       key="show_sharpe",      on_change=on_sharpe)
        show_growth_rate = st.toggle("Time-average growth rate contour",   key="show_growth_rate", on_change=on_growth)
    
    show_assets = True

    #Setting parameters for the model
    rf = 0.05
    ret_min = 0.06 
    risk_min = 0.15
    curvature = 15

    sigma_max = 0.6
    mu_max = 0.30

    # --- Efficient Frontier (sideways parabola) ---
    ret_range = np.linspace(ret_min, mu_max, 300)
    risk_curve = risk_min + curvature * (ret_range - ret_min) ** 2

    # Lower (inefficient) half
    ret_lower = np.linspace(ret_min - 0.05, ret_min, 100)
    risk_lower = risk_min + curvature * (ret_lower - ret_min) ** 2

    # --- Tangency Portfolio & CAL ---
    sharpe = (ret_range - rf) / risk_curve
    tang_idx = np.argmax(sharpe)
    tang_risk = risk_curve[tang_idx]
    tang_ret = ret_range[tang_idx]

    slope = (tang_ret - rf) / tang_risk
    cal_risks = np.linspace(0, sigma_max, 200)
    cal_returns = rf + slope * cal_risks

    # --- Individual Assets ---
    np.random.seed(42)
    asset_risks   = [0.22, 0.28, 0.32, 0.26, 0.30, 0.25, 0.35, 0.20]
    asset_returns = [0.06, 0.07, 0.14, 0.12, 0.11, 0.08, 0.17, 0.09]

    # --- Plot ---
    fig, ax = plt.subplots( figsize=(9, 3.6))
    
    if show_sharpe:
        show_assets = False

        risk_g = np.linspace(0.001, sigma_max, 200)
        ret_g  = np.linspace(0.00, mu_max, 200)
        RISK, RET = np.meshgrid(risk_g, ret_g)
        SHARPE = (RET - rf) / RISK

        levels = [slope * f for f in [-3, -2, -1.5, -1, -0.75,-0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3]]
        levels =  [-0.5, -0.25, 0, 0.25, 0.5, 1, 2, 3 ]
        cmap_trunc = mcolors.LinearSegmentedColormap.from_list(
                "Greys_trunc", plt.cm.Greys(np.linspace(0.01, 0.5, 256))
                )

        norm = mcolors.Normalize(vmin=levels[0], vmax=levels[-1])
        #cf   = ax.contourf(RISK, RET, SHARPE, levels=levels, cmap=cmap_trunc, norm=norm)
        cs   = ax.contour(RISK, RET, SHARPE, levels=levels, colors="grey", linewidths=0.5, alpha=0.6)
        ax.clabel(cs, fmt=lambda x: rf"Sharpe = {x:.2f}", fontsize=7, inline=True)
        if show_CML:
            ax.annotate(rf"Sharpe = {slope:.2f}", xy=(0.45, rf + slope * 0.45),
                    xytext=(0.45, rf + slope * 0.45 + 0.04),
                    fontsize=9)

        with col1:
            st.markdown('<p class="subheader">Markowitz / Sharpe:</p>', unsafe_allow_html=True)
            st.markdown(markdown1)

    if show_growth_rate:
        show_assets = False
        
        risk_g = np.linspace(0.001, sigma_max, 200)
        ret_g  = np.linspace(0.00, mu_max, 200)
        RISK, RET = np.meshgrid(risk_g, ret_g)

        GR = RET - RISK**2/2
        optimal_lev = (tang_ret-rf) / tang_risk**2
        optimal_gr = rf + optimal_lev*(tang_ret-rf) - optimal_lev**2*tang_risk**2/2
        mu_opt = rf + optimal_lev*(tang_ret-rf)
        sigma_opt = np.sqrt(optimal_lev**2*tang_risk**2)

        ax.scatter(sigma_opt,mu_opt, label = f"Optimally leveraged portfolio",zorder=10, s= 70, color=COLORS["green"])
        ax.annotate("Optimally leveraged\nPortfolio", xy=(sigma_opt, mu_opt),
                    xytext=(sigma_opt - 0.04, mu_opt + 0.015),
                    color = COLORS["green"], fontsize=9)
        
        levels = [-0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25]
    
        cs   = ax.contour(RISK, RET, GR, levels=levels, colors="grey", linewidths=0.5, alpha=0.6)
        cs_opt   = ax.contour(RISK, RET, GR, levels=[optimal_gr], colors="black", linestyle= "--", linewidths=0.7)
        ax.clabel(cs, fmt=lambda x: f"g ={x:.2f}", fontsize=8, inline=True)         

        with col1:
            st.markdown('<p class="subheader">Markowitz / Sharpe:</p>', unsafe_allow_html=True)
            st.markdown(markdown1)
            st.markdown('<p class="subheader">Ergodicity Economics:</p>', unsafe_allow_html=True)
            st.markdown(markdown2)  

    if show_frontier:

        ax.plot(risk_lower, ret_lower, color=COLORS["inefficient_frontier"], lw=2, linestyle="--", label="Inefficient Frontier")
        ax.plot(risk_curve, ret_range, color=COLORS["inefficient_frontier"], lw=2.5, label="Efficient Frontier")
        ax.annotate("Efficient Frontier", xy=(risk_curve[220], ret_range[220]),
                    xytext=(risk_curve[220] - 0.02, ret_range[220] - 0.023),
                    fontsize=9, color=COLORS["efficient_frontier"])
    
    if show_riskfree:
        ax.scatter([0], [rf], color="black", s=80, marker= "x", zorder=6)
        ax.text(0.005, rf - 0.008, "Risk-Free Asset", fontsize=9)

    if show_CML:
        ax.plot(cal_risks, cal_returns, color="black", lw=2, label="Capital Market Line")
        ax.scatter([tang_risk], [tang_ret], color=COLORS["tangency"], s=70, zorder=6, label="Tangency Portfolio")
        ax.annotate("Tangency\nPortfolio", xy=(tang_risk, tang_ret),
                    xytext=(tang_risk - 0.03, tang_ret + 0.015),
                    color = COLORS["tangency"], fontsize=9)
        ax.annotate("Capital Market Line", xy=(0.45, rf + slope * 0.45),
                    xytext=(0.45, rf + slope * 0.45 + 0.055),
                    fontsize=9)
    
    if show_assets:
        ax.scatter(asset_risks, asset_returns, color=COLORS["assets"], s=50, zorder=5, marker="x", label="Individual Assets")
        ax.text(0.27, 0.085, "Individual Assets", fontsize=9, color=COLORS["assets"])
          
    ax.set_xlabel("Volatility, $\sigma$")
    ax.set_ylabel("Drift, $\mu$")
    #ax.set_title("Markowitz Portfolio Theory", fontsize=14, fontweight="bold")
    ax.set_xlim(-0.01, sigma_max)
    ax.set_ylim(0.0, mu_max)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), fontsize=9)
    
    fig.subplots_adjust(wspace=0.3)
    
    with col2:
        st.pyplot(fig)

    # --- Key metrics ---
    '''
    col1, col2, col3 = st.columns(3)
    col1.metric("Optimal leverage", f"{(tang_ret-rf)/tang_risk**2:.1%}")  
    col1.metric("Sharpe ratio", f"{(tang_ret-rf)/tang_risk:.2%}")    
    col1.metric("Risk-Free Rate", f"{rf:.1%}")
    col2.metric("Tangency Portfolio Return", f"{tang_ret:.1%}")
    col3.metric("Tangency Portfolio Risk (σ)", f"{tang_risk:.1%}")
    st.caption(f"Sharpe Ratio of Tangency Portfolio: **{(tang_ret - rf) / tang_risk:.2f}**")
    '''
    plt.close(fig)



#----------------------------------------
# Slide definitions
#----------------------------------------

APP_SLIDES: dict = {
    "leverage": app_slide_leverage,
    "markowitz": app_slide_markowitz,
}





# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
    ("pdf", 0),             # title page
    ("pdf", 1),             # Content of markets talks
    ("pdf", 2),             # Content of markets talks
    ("pdf", 3),             # GBM
    ("pdf", 4),             # Portfolio problem
    ("pdf", 5),             # Optimal Portfolio
    ("app", "leverage"),    # interactive Brownian motion
    ("pdf", 6),             # Optimal Portfolio
    ("app", "markowitz"),   # interactive Brownian motion
    ("pdf", 7),             # thank you
]