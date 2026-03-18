"""Slide 4: Multiplicative dynamic with moving measurement window.

x(t) = x(0)·α^t — an exponential.  The same fixed-width window gives a
dramatically different δx depending on where it is placed, showing that
the additive clock is the wrong clock for multiplicative dynamics.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import (
    LML_BLUE, LML_GREY, BERNOULLI, PANEL_BG, PANEL_BORDER,
    render_slide_header, draw_window_annotation,
)

T_MAX = 6.0
N_PTS = 400
T = np.linspace(0, T_MAX, N_PTS)

G = 0.30        # log-growth: x(t) = exp(G·t)
X0 = 1.0
WIN_WIDTH = 2.0

PATH_COLOR = LML_BLUE


def multiplicative_window_slide() -> None:
    render_slide_header("Multiplicative dynamics: same clock tick, different growth")

    t0 = st.slider(
        "← Shift measurement window →",
        min_value=0.0,
        max_value=T_MAX - WIN_WIDTH,
        value=1.0,
        step=0.1,
        key="mul_t0",
    )

    x = X0 * np.exp(G * T)
    x0_val = X0 * np.exp(G * t0)
    x1_val = X0 * np.exp(G * (t0 + WIN_WIDTH))
    delta_x = x1_val - x0_val

    col_formula, col_plot = st.columns([2.8, 6.2])

    with col_formula:
        st.markdown(
            f"""
<div style="background:#FEF2F2;border:1px solid #FCA5A5;
  border-left:6px solid {PATH_COLOR};border-radius:0.4rem;
  padding:0.9rem 1rem;margin-top:0.4rem">
  <b style="color:{PATH_COLOR}">Multiplicative dynamic</b><br><br>
  <span style="font-family:monospace">x(t+1) = x(t) · α</span><br>
  <span style="font-family:monospace">x(t) &nbsp;= α<sup>t</sup> · x(0)</span><br>
  <br>
  <span style="color:{LML_GREY};font-size:0.85rem">
    Window: t = {t0:.1f} → {t0 + WIN_WIDTH:.1f}<br>
    δt = {WIN_WIDTH:.0f}
  </span><br><br>
  <b style="color:{BERNOULLI};font-size:1.15rem">δx = {delta_x:.2f}</b>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_plot:
        fig, ax = plt.subplots(figsize=(8.0, 3.6))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(T, x, color=PATH_COLOR, lw=2.8)

        y_bot, y_top = draw_window_annotation(
            ax, t0, WIN_WIDTH, x0_val, x1_val,
            y_floor=0.0, y_max_val=float(x.max()),
            color=BERNOULLI,
            delta_label=f"δx = {delta_x:.2f}",
        )

        ax.set_xlim(-0.2, T_MAX + 1.5)
        ax.set_ylim(y_bot, y_top)
        ax.set_xlabel("time  t", fontsize=10, color=LML_BLUE)
        ax.set_ylabel("wealth  x(t)", fontsize=10, color=LML_BLUE)
        ax.set_title(
            "x(t) = α^t · x(0)    (multiplicative dynamic)",
            fontsize=11, color=LML_BLUE, fontweight="bold",
        )
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines["left"].set_color("#9CA3AF")
        ax.spines["bottom"].set_color("#9CA3AF")
        ax.tick_params(colors="#374151")
        ax.grid(axis="x", color="#E5E7EB", lw=0.8)

        plt.tight_layout(pad=0.6)
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
