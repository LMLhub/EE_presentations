"""
Slide deck definition for this presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_demo() -> None:
    """A trivial interactive slide: a configurable sine wave."""
    st.subheader("Interactive Demo Slide")
    col1, col2 = st.columns(2)
    with col1:
        freq = st.slider("Frequency", 0.5, 5.0, 1.0, 0.1)
    with col2:
        amp = st.slider("Amplitude", 0.1, 2.0, 1.0, 0.1)

    x = np.linspace(0, 2 * np.pi, 500)
    y = amp * np.sin(freq * x)

    fig, ax = plt.subplots(figsize=(7, 3))
    ax.plot(x, y, lw=2)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"y = {amp:.1f} · sin({freq:.1f}x)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_coin_toss() -> None:
    """Peters coin toss: trajectory, expected value, and time-average growth."""
    st.markdown("""
    <style>
    div[data-testid="stButton"] button { font-size: 50px !important; padding: 0.4rem 1.2rem; }
    /* Hide the built-in thumb value and tick labels — we render the value ourselves */
    div[data-testid="stSlider"] p { display: none !important; }
    /* Left padding for the whole app */
    section[data-testid="stMain"] > div { padding-left: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Peters Coin Toss")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<p style="font-size:30px; margin-bottom:0">Number of rounds</p>',
                    unsafe_allow_html=True)
        nr_min, nr_max = 10, 1000
        n_rounds = st.slider("Number of rounds", nr_min, nr_max, 200, 10, label_visibility="collapsed")
        nr_frac = (n_rounds - nr_min) / (nr_max - nr_min)
        st.markdown(
            f'<div style="position:relative;height:36px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:20px;color:#999;">{nr_min}</span>'
            f'<span style="position:absolute;left:calc({nr_frac*100:.2f}% - {nr_frac*20:.2f}px + 10px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">{n_rounds}</span>'
            f'<span style="position:absolute;right:0;font-size:20px;color:#999;">{nr_max}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.write("")  # vertical alignment spacer
        run = st.button("Run")

    # Multiplicative factors: ×1.5 (heads) or ×0.6 (tails), fair coin
    # Expected value growth:  E[W_n] = (0.5·1.5 + 0.5·0.6)^n = 1.05^n
    # Time-average growth rate: γ = 0.5·ln(1.5) + 0.5·ln(0.6) ≈ −0.053/round
    gamma = 0.5 * np.log(1.5) + 0.5 * np.log(0.6)

    key = "coin_toss_traj"
    if run or key not in st.session_state or len(st.session_state[key]) != n_rounds + 1:
        flips = np.random.choice([1.5, 0.6], size=n_rounds)
        st.session_state[key] = np.cumprod(np.concatenate([[1.0], flips]))

    traj = st.session_state[key]
    n = np.arange(n_rounds + 1)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(n, traj, color="#004670", lw=1.2, alpha=0.85, label="Trajectory")
    ax.semilogy(n, 1.05 ** n, color="#e07000", lw=2)
    ax.semilogy(n, np.exp(gamma * n), color="#2a9d8f", lw=2, ls="--")
    ax.set_xlabel("round $t$")
    ax.set_ylabel("wealth $x$")
    ax.grid(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    # Set y-limits so both straight lines are fully visible and 1 is centred
    upper_decades = n_rounds * np.log10(1.05)
    lower_decades = n_rounds * abs(gamma) / np.log(10)
    half_range = max(upper_decades, lower_decades) * 1.2
    half_range = max(half_range, 1)
    ax.set_ylim(10 ** -half_range, 10 ** half_range)
    # Remove left-margin padding so the y-axis sits exactly at n=0
    ax.set_xlim(0, n_rounds)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_leverage() -> None:
    """Leveraged coin toss: vary fraction of wealth exposed to the gamble."""
    st.markdown("""
    <style>
    div[data-testid="stButton"] button { font-size: 50px !important; padding: 0.4rem 1.2rem; }
    div[data-testid="stSlider"] p { display: none !important; }
    section[data-testid="stMain"] > div { padding-left: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Leveraged Coin Toss")

    # Base coin: heads ×1.5, tails ×0.6 at leverage l=1.
    # At leverage l the round multiplier is:
    #   heads: 1 + l·0.5   tails: 1 - l·0.4
    # Expected value growth rate per round: 1 + 0.05·l
    # Time-average growth rate: γ(l) = 0.5·ln(1+0.5l) + 0.5·ln(1-0.4l)
    #   defined only while both factors are positive: l < 2.5 and l > -2

    n_rounds = 500

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<p style="font-size:30px; margin-bottom:0">Leverage</p>',
                    unsafe_allow_html=True)
        lev_min, lev_max = -3.0, 3.0
        leverage = st.slider("Leverage", lev_min, lev_max, 1.0, 0.05,
                             label_visibility="collapsed")
        lev_frac = (leverage - lev_min) / (lev_max - lev_min)
        st.markdown(
            f'<div style="position:relative;height:36px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:20px;color:#999;">{lev_min:.1f}</span>'
            f'<span style="position:absolute;left:calc({lev_frac*100:.2f}% - {lev_frac*20:.2f}px + 10px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">{leverage:.2f}</span>'
            f'<span style="position:absolute;right:0;font-size:20px;color:#999;">{lev_max:.1f}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.write("")
        run = st.button("Run")

    heads_factor = 1.0 + 0.5 * leverage
    tails_factor = 1.0 - 0.4 * leverage
    ev_factor = 0.5 * heads_factor + 0.5 * tails_factor  # = 1 + 0.05·l

    # Time-average growth rate — only real when both factors are positive
    gamma_defined = heads_factor > 0 and tails_factor > 0
    if gamma_defined:
        gamma = 0.5 * np.log(heads_factor) + 0.5 * np.log(tails_factor)

    key = "leverage_traj"
    traj_key = (n_rounds, round(leverage, 3))
    if run or key not in st.session_state or st.session_state.get(key + "_params") != traj_key:
        rng = np.random.default_rng()
        factors = np.where(rng.random(n_rounds) < 0.5, heads_factor, tails_factor)
        # Track ruinous outcomes: clamp wealth at a tiny floor
        wealth = np.empty(n_rounds + 1)
        wealth[0] = 1.0
        for i, f in enumerate(factors):
            wealth[i + 1] = max(wealth[i] * f, 1e-60)
            if wealth[i] <= 1e-58:
                wealth[i + 1:] = 1e-60
                break
        st.session_state[key] = wealth
        st.session_state[key + "_params"] = traj_key

    traj = st.session_state[key]
    n = np.arange(n_rounds + 1)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(n, traj, color="#004670", lw=1.2, alpha=0.85)
    ax.semilogy(n, ev_factor ** n, color="#e07000", lw=2)
    if gamma_defined:
        ax.semilogy(n, np.exp(gamma * n), color="#2a9d8f", lw=2, ls="--")

    ax.set_xlabel("round $t$")
    ax.set_ylabel("wealth $x$")
    ax.grid(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    upper_decades = n_rounds * np.log10(max(ev_factor, 1.0001))
    lower_decades = n_rounds * abs(gamma if gamma_defined else 0.05) / np.log(10)
    half_range = max(upper_decades, lower_decades) * 1.2
    half_range = max(half_range, 1)
    ax.set_ylim(10 ** -half_range, 10 ** half_range)
    ax.set_xlim(0, n_rounds)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_cooperation() -> None:
    """Cooperating coin toss: N players pool and split wealth each round."""
    from math import comb

    st.markdown("""
    <style>
    div[data-testid="stButton"] button { font-size: 50px !important; padding: 0.4rem 1.2rem; }
    div[data-testid="stSlider"] p { display: none !important; }
    section[data-testid="stMain"] > div { padding-left: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Cooperating Coin Toss")

    n_rounds = 500

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<p style="font-size:30px; margin-bottom:0">Number of players</p>',
                    unsafe_allow_html=True)
        np_min, np_max = 1, 10
        n_players = st.slider("Number of players", np_min, np_max, 1, 1,
                              label_visibility="collapsed")
        np_frac = (n_players - np_min) / (np_max - np_min)
        st.markdown(
            f'<div style="position:relative;height:36px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:20px;color:#999;">{np_min}</span>'
            f'<span style="position:absolute;left:calc({np_frac*100:.2f}% - {np_frac*20:.2f}px + 10px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">{n_players}</span>'
            f'<span style="position:absolute;right:0;font-size:20px;color:#999;">{np_max}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.write("")
        run = st.button("Run")

    # Time-average growth rate for N cooperative players:
    # Each round the shared multiplier = mean of N iid flips (1.5 or 0.6).
    # k heads out of N:  multiplier = (1.5k + 0.6(N-k)) / N
    # γ_N = Σ_{k=0}^{N} C(N,k)/2^N · ln((1.5k + 0.6(N-k)) / N)
    gamma = sum(
        comb(n_players, k) / 2 ** n_players
        * np.log((1.5 * k + 0.6 * (n_players - k)) / n_players)
        for k in range(n_players + 1)
    )

    key = "coop_traj"
    traj_params = (n_rounds, n_players)
    if run or key not in st.session_state or st.session_state.get(key + "_params") != traj_params:
        rng = np.random.default_rng()
        wealth = np.empty(n_rounds + 1)
        wealth[0] = 1.0
        for t in range(n_rounds):
            flips = np.where(rng.random(n_players) < 0.5, 1.5, 0.6)
            wealth[t + 1] = wealth[t] * flips.mean()
        st.session_state[key] = wealth
        st.session_state[key + "_params"] = traj_params

    traj = st.session_state[key]
    n = np.arange(n_rounds + 1)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(n, traj, color="#004670", lw=1.2, alpha=0.85)
    ax.semilogy(n, 1.05 ** n, color="#e07000", lw=2)
    ax.semilogy(n, np.exp(gamma * n), color="#2a9d8f", lw=2, ls="--")

    ax.set_xlabel("round $t$")
    ax.set_ylabel("wealth $x$")
    ax.grid(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    upper_decades = n_rounds * np.log10(1.05)
    lower_decades = n_rounds * abs(gamma) / np.log(10)
    half_range = max(upper_decades, lower_decades) * 1.2
    half_range = max(half_range, 1)
    ax.set_ylim(10 ** -half_range, 10 ** half_range)
    ax.set_xlim(0, n_rounds)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_redistribution() -> None:
    """Coin toss with proportional tax τ and equal redistribution."""
    st.markdown("""
    <style>
    div[data-testid="stButton"] button { font-size: 50px !important; padding: 0.4rem 1.2rem; }
    div[data-testid="stSlider"] p { display: none !important; }
    section[data-testid="stMain"] > div { padding-left: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Coin Toss with Redistribution")

    # N players, each flips independently, then each pays fraction τ of their
    # post-flip wealth into a pot that is split equally.
    # Per-round wealth update:  x_i' = (1-τ)·f_i·x_i + τ·mean_j(f_j·x_j)
    #
    # In the large-N limit (LLN: mean flip → 1.05, mean wealth → x̄):
    #   effective multiplier for player i ≈ (1-τ)·f_i + τ·1.05
    #   γ(τ) = ½·ln(1.5 - 0.45τ) + ½·ln(0.6 + 0.45τ)
    # τ=0 → individual coin toss,  τ=1 → full cooperation (= cooperation slide)

    N_PLAYERS = 100   # large enough for LLN to be visible
    n_rounds = 500

    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<p style="font-size:30px; margin-bottom:0">Tax / redistribution fraction τ</p>',
                    unsafe_allow_html=True)
        tau_min, tau_max = -0.1, 0.1
        tau = st.slider("tau", tau_min, tau_max, 0.0, 0.01, label_visibility="collapsed")
        tau_frac = (tau - tau_min) / (tau_max - tau_min)
        st.markdown(
            f'<div style="position:relative;height:40px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:30px;color:#999;">{tau_min:.2f}</span>'
            f'<span style="position:absolute;left:calc({tau_frac*100:.2f}% - {tau_frac*20:.2f}px + 10px);transform:translateX(-50%);font-size:30px;color:#555;white-space:nowrap;">τ = {tau:.2f}</span>'
            f'<span style="position:absolute;right:0;font-size:30px;color:#999;">{tau_max:.2f}</span>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.write("")
        run = st.button("Run")

    # Time-average growth rate (large-N limit)
    h = 1.5 - 0.45 * tau   # effective heads multiplier
    t_ = 0.6 + 0.45 * tau  # effective tails multiplier
    gamma = 0.5 * np.log(h) + 0.5 * np.log(t_)

    key = "redist_traj"
    traj_params = (n_rounds, round(tau, 3))
    if run or key not in st.session_state or st.session_state.get(key + "_params") != traj_params:
        rng = np.random.default_rng()
        # Track all N_PLAYERS trajectories
        all_w = np.ones(N_PLAYERS)
        wealth = np.empty((N_PLAYERS, n_rounds + 1))
        wealth[:, 0] = 1.0
        for step in range(n_rounds):
            flips = np.where(rng.random(N_PLAYERS) < 0.5, 1.5, 0.6)
            post_flip = all_w * flips
            pool = tau * post_flip.mean()
            all_w = (1.0 - tau) * post_flip + pool
            wealth[:, step + 1] = all_w
        st.session_state[key] = wealth
        st.session_state[key + "_params"] = traj_params

    wealth = st.session_state[key]
    n = np.arange(n_rounds + 1)

    fig, ax = plt.subplots(figsize=(9, 4))
    for traj in wealth:
        ax.semilogy(n, traj, color="#004670", lw=0.6, alpha=0.5)
    ax.semilogy(n, 1.05 ** n, color="#e07000", lw=2)
    ax.semilogy(n, np.exp(gamma * n), color="#2a9d8f", lw=2, ls="--")

    ax.set_xlabel("round $t$")
    ax.set_ylabel("wealth $x$")
    ax.grid(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    upper_decades = n_rounds * np.log10(1.05)
    lower_decades = n_rounds * max(abs(gamma), 1e-6) / np.log(10)
    half_range = max(upper_decades, lower_decades) * 1.2
    half_range = max(half_range, 1)
    ax.set_ylim(10 ** -half_range, 10 ** half_range)
    ax.set_xlim(0, n_rounds)
    st.pyplot(fig)
    plt.close(fig)


def app_slide_isoelastic() -> None:
    """Deterministic growth: two (γ, x₀) pairs, one η slider."""
    st.markdown("""
    <style>
    div[data-testid="stSlider"] p { display: none !important; }
    section[data-testid="stMain"] > div { padding-left: 4rem !important; padding-right: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Deterministic Growth")

    CASES = [
        {"gamma": 0.1, "x0": 2.0, "color": "#004670", "label": r"$\gamma=0.1,\ x_0=2$"},
        {"gamma": 0.2, "x0": 1.0, "color": "#c82828", "label": r"$\gamma=0.2,\ x_0=1$"},
    ]
    T = 10.0
    EPS = 0.026  # half a slider step — used to detect η=1 special case

    eta_min, eta_max = -1.0, 3.0
    eta = st.slider("eta", eta_min, eta_max, 1.0, 0.05, label_visibility="collapsed")
    eta_frac = (eta - eta_min) / (eta_max - eta_min)
    st.markdown(
        f'<div style="position:relative;height:36px;margin-top:-8px;">'
        f'<span style="position:absolute;left:0;font-size:28px;color:#999;">{eta_min:.1f}</span>'
        f'<span style="position:absolute;left:calc({eta_frac*100:.2f}% - {eta_frac*28:.2f}px + 14px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">η = {eta:.2f}</span>'
        f'<span style="position:absolute;right:0;font-size:28px;color:#999;">{eta_max:.1f}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

    is_mult = abs(eta - 1.0) < EPS  # η=1: multiplicative / ln special case

    def compute(gamma, x0):
        t_end = T
        if not is_mult and eta > 1.0:
            t_star = x0 ** (1.0 - eta) / ((eta - 1.0) * gamma)
            t_end = min(T, 0.95 * t_star)
        t = np.linspace(0, t_end, 800)
        if is_mult:
            x_t = x0 * np.exp(gamma * t)
            v_t = np.log(x_t)
            v0  = np.log(x0)
        else:
            ome = 1.0 - eta
            arg = np.maximum(x0 ** ome + ome * gamma * t, 1e-300)
            x_t = arg ** (1.0 / ome)
            v_t = x_t ** ome / ome
            v0  = x0  ** ome / ome
        v_linear = gamma * t + v0
        return t, x_t, v_t, v_linear

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True,
                                   gridspec_kw={"hspace": 0.45})
    fig.subplots_adjust(right=0.82)

    for c in CASES:
        t, x_t, v_t, v_linear = compute(c["gamma"], c["x0"])
        ax1.plot(t, x_t, color=c["color"], lw=2, label=c["label"])
        ax2.plot(t, v_t, color=c["color"], lw=2, label=c["label"])

    ax1.set_ylabel("$x(t)$", fontsize=13)
    ax1.legend(fontsize=11, frameon=False, loc="upper left")
    ax1.spines["right"].set_visible(False)
    ax1.spines["top"].set_visible(False)

    ax2.set_xlabel("$t$", fontsize=13)
    ax2.set_ylabel(r"$v\!\left(x(t)\right)$", fontsize=13)
    ax2.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    st.pyplot(fig)
    plt.close(fig)


def app_slide_stochastic_growth() -> None:
    """Stochastic isoelastic process: dv = γ dt + σ dW, x(t) = v⁻¹(v(t))."""
    st.markdown("""
    <style>
    div[data-testid="stButton"] button { font-size: 50px !important; padding: 0.4rem 1.2rem; }
    div[data-testid="stSlider"] p { display: none !important; }
    section[data-testid="stMain"] > div { padding-left: 4rem !important; padding-right: 4rem !important; }
    </style>
    """, unsafe_allow_html=True)

    st.subheader("Stochastic Growth")

    CASES = [
        {"gamma": 0.1, "x0": 2.0, "color": "#004670", "color_v": "#004670", "label": r"$\gamma=0.1,\ x_0=2$"},
        {"gamma": 0.2, "x0": 1.0, "color": "#c82828", "color_v": "#c82828", "label": r"$\gamma=0.2,\ x_0=1$"},
    ]
    dt = 0.01
    T = 50.0
    N = int(T / dt)
    EPS = 0.026

    # ── Sliders ──────────────────────────────────────────────────────────
    col_eta, col_gap, col_sigma, col_btn = st.columns([4, 0.5, 4, 1])

    with col_eta:
        eta_min, eta_max = -1.0, 3.0
        eta = st.slider("eta_s", eta_min, eta_max, 1., 0.05, label_visibility="collapsed")
        eta_frac = (eta - eta_min) / (eta_max - eta_min)
        st.markdown(
            f'<div style="position:relative;height:36px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:28px;color:#999;">{eta_min:.1f}</span>'
            f'<span style="position:absolute;left:calc({eta_frac*100:.2f}% - {eta_frac*28:.2f}px + 14px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">\u03b7 = {eta:.2f}</span>'
            f'<span style="position:absolute;right:0;font-size:28px;color:#999;">{eta_max:.1f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_sigma:
        sig_min, sig_max = 0.0, 1.0
        sigma = st.slider("sigma_s", sig_min, sig_max, 0., 0.05, label_visibility="collapsed")
        sig_frac = (sigma - sig_min) / (sig_max - sig_min)
        st.markdown(
            f'<div style="position:relative;height:36px;margin-top:-8px;">'
            f'<span style="position:absolute;left:0;font-size:28px;color:#999;">{sig_min:.1f}</span>'
            f'<span style="position:absolute;left:calc({sig_frac*100:.2f}% - {sig_frac*28:.2f}px + 14px);transform:translateX(-50%);font-size:28px;color:#555;white-space:nowrap;">\u03c3 = {sigma:.2f}</span>'
            f'<span style="position:absolute;right:0;font-size:28px;color:#999;">{sig_max:.1f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with col_btn:
        st.write("")
        run = st.button("\u25b6")

    is_mult = abs(eta - 1.0) < EPS
    ome = 1.0 - eta  # only used when not is_mult

    # Clipping at 0.95·t* (same logic as deterministic slide)
    if not is_mult and eta > 1.0:
        t_end = min(
            min(0.95 * c["x0"] ** (1.0 - eta) / ((eta - 1.0) * c["gamma"]) for c in CASES),
            T,
        )
    else:
        t_end = T

    def v_of_x(x):
        return float(np.log(x) if is_mult else x ** ome / ome)

    def invert_v(v_arr):
        if is_mult:
            return np.exp(v_arr)
        arg = ome * v_arr
        return np.where(arg > 1e-300, arg ** (1.0 / ome), np.nan)

    # ── Simulate or reuse cached trajectories ────────────────────────────
    key = "stoch_traj"
    params = (round(eta, 3), round(sigma, 3))
    if run or key not in st.session_state or st.session_state.get(key + "_p") != params:
        rng = np.random.default_rng()
        trajs = {}
        for c in CASES:
            v0 = v_of_x(c["x0"])
            dv = c["gamma"] * dt + sigma * np.sqrt(dt) * rng.standard_normal(N)
            v_arr = np.empty(N + 1)
            v_arr[0] = v0
            v_arr[1:] = v0 + np.cumsum(dv)
            trajs[c["label"]] = (v0, c["gamma"], v_arr)
        st.session_state[key] = trajs
        st.session_state[key + "_p"] = params

    trajs = st.session_state[key]
    t = np.linspace(0, T, N + 1)

    # Truncate for display
    n_plot = min(int(t_end / dt) + 1, N + 1)
    t_plot = t[:n_plot]

    # ── Plots ─────────────────────────────────────────────────────────────
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5), sharex=True,
                                   gridspec_kw={"hspace": 0.45})
    fig.subplots_adjust(right=0.92)

    for c in CASES:
        v0, gamma, v_arr = trajs[c["label"]]
        v_det = gamma * t_plot + v0
        x_det = invert_v(v_det)
        x_arr = invert_v(v_arr[:n_plot])
        ax1.plot(t_plot, x_det, color=c["color"], lw=1.5, ls="--")
        ax1.plot(t_plot, x_arr, color=c["color"], lw=1.2, label=c["label"])
        ax2.plot(t_plot, v_det, color=c["color"], lw=1.5, ls="--")
        ax2.plot(t_plot, v_arr[:n_plot], color=c["color"], lw=1.2)

    ax1.set_ylabel("$x(t)$", fontsize=13)
    ax1.legend(fontsize=11, frameon=False, loc="upper left")
    ax1.spines["right"].set_visible(False)
    ax1.spines["top"].set_visible(False)

    ax2.set_xlabel("$t$", fontsize=13)
    ax2.set_ylabel(r"$v\!\left(x(t)\right)$", fontsize=13)
    ax2.spines["right"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    st.pyplot(fig)
    plt.close(fig)


APP_SLIDES: dict = {
    "coin-toss": app_slide_coin_toss,
    "leverage": app_slide_leverage,
    "cooperation": app_slide_cooperation,
    "redistribution": app_slide_redistribution,
    "isoelastic": app_slide_isoelastic,
    "stochastic-growth": app_slide_stochastic_growth,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
def pdf_pages(spec) -> list[tuple[str, int]]:
    """Expand a PDF page spec into a list of ("pdf", index) tuples.

    spec can be:
      - an int          -> single page, e.g. pdf_pages(0)
      - a "start-end"   -> inclusive range, e.g. pdf_pages("0-4")
      - a list mixing the above, e.g. pdf_pages([0, "3-5", 8])
    Page indices are 0-based.
    """
    if isinstance(spec, list):
        result = []
        for item in spec:
            result.extend(pdf_pages(item))
        return result
    if isinstance(spec, str) and "-" in spec:
        start, end = spec.split("-")
        return [("pdf", i) for i in range(int(start), int(end) + 1)]
    return [("pdf", int(spec))]


SLIDES: list = [
    *pdf_pages("0-7"),
    ("app", "isoelastic"),          # deterministic isoelastic process
    *pdf_pages("8-11"),
    ("app", "stochastic-growth"),  # stochastic isoelastic process
    *pdf_pages("12-40")
]
