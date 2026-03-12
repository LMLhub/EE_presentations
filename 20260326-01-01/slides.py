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
        n_rounds = st.slider("Number of rounds", 10, 1000, 200, 10, label_visibility="collapsed")
        st.markdown(f'<p style="font-size:28px; margin-top:0; color:#555;">{n_rounds}</p>',
                    unsafe_allow_html=True)
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
        leverage = st.slider("Leverage", -3.0, 3.0, 1.0, 0.05,
                             label_visibility="collapsed")
        st.markdown(f'<p style="font-size:28px; margin-top:0; color:#555;">{leverage:.2f}</p>',
                    unsafe_allow_html=True)
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
        n_players = st.slider("Number of players", 1, 10, 1, 1,
                              label_visibility="collapsed")
        st.markdown(f'<p style="font-size:28px; margin-top:0; color:#555;">{n_players}</p>',
                    unsafe_allow_html=True)
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
        sub1, sub2, sub3 = st.columns([1, 2, 1])
        with sub1:
            st.markdown(f'<p style="font-size:30px; color:#999;">{tau_min:.2f}</p>',
                        unsafe_allow_html=True)
        with sub2:
            st.markdown(f'<p style="font-size:30px; text-align:center; color:#555;">τ = {tau:.2f}</p>',
                        unsafe_allow_html=True)
        with sub3:
            st.markdown(f'<p style="font-size:30px; color:#999; text-align:right;">{tau_max:.2f}</p>',
                        unsafe_allow_html=True)
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


APP_SLIDES: dict = {
    "coin-toss": app_slide_coin_toss,
    "leverage": app_slide_leverage,
    "cooperation": app_slide_cooperation,
    "redistribution": app_slide_redistribution,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
    ("pdf", 0),             # title page
#    ("pdf", 1),             # wealth vs. time figure
    ("app", "coin-toss"),       # Peters coin toss
    ("app", "leverage"),        # leveraged coin toss
    ("app", "cooperation"),     # cooperating coin toss
    ("app", "redistribution"),  # tax and redistribute
#    ("pdf", 2),             # thank you / Galton board
]
