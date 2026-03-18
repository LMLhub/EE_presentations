"""Slide 4tris: Apply the ergodic transform — ln(x) gives a steady clock.

Solution 2: instead of changing clock speed, transform the wealth axis.
For multiplicative dynamics, ln(x(t)) = G·t is a straight line.
A fixed window gives constant δ(ln x) everywhere — the log clock is steady.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import (
    LML_BLUE, LML_GREY, FERMAT, PANEL_BG, PANEL_BORDER,
    render_slide_header, draw_window_annotation,
)

T_MAX = 6.0
N_PTS = 400
T = np.linspace(0, T_MAX, N_PTS)

G = 0.30     # log-growth rate: ln x(t) = G·t  (x(t) = exp(G·t))
X0 = 1.0
WIN_WIDTH = 2.0

PATH_COLOR = FERMAT  # green for the "correct" ergodic transform


def log_transform_slide() -> None:
    render_slide_header("Solution 2: transform wealth — ln(x) gives constant increments")

    t0 = st.slider(
        "← Shift measurement window →",
        min_value=0.0,
        max_value=T_MAX - WIN_WIDTH,
        value=2.0,
        step=0.1,
        key="log_t0",
    )

    ln_x = G * T + np.log(X0)    # ln(x(t)) — straight line
    ln_x0 = G * t0 + np.log(X0)
    ln_x1 = G * (t0 + WIN_WIDTH) + np.log(X0)
    delta_ln_x = ln_x1 - ln_x0   # always = G * WIN_WIDTH

    col_formula, col_plot = st.columns([2.8, 6.2])

    with col_formula:
        st.markdown(
            f"""
<div style="background:{PANEL_BG};border:1px solid {PANEL_BORDER};
  border-left:6px solid {PATH_COLOR};border-radius:0.4rem;
  padding:0.9rem 1rem;margin-top:0.4rem">
  <b style="color:{PATH_COLOR}">Multiplicative dynamic — log clock</b><br><br>
  <span style="font-family:monospace">x(t+1) = x(t) · α</span><br>
  <span style="font-family:monospace">x(t) &nbsp;= α<sup>t</sup> · x(0)</span><br>
  <span style="font-family:monospace">ln x(t) = t·ln α + ln x(0)</span><br>
  <br>
  <span style="color:{LML_GREY};font-size:0.85rem">
    Window: t = {t0:.1f} → {t0 + WIN_WIDTH:.1f}<br>
    δt = {WIN_WIDTH:.0f}
  </span><br><br>
  <b style="color:{PATH_COLOR};font-size:1.15rem">δ(ln x) = {delta_ln_x:.2f}</b><br>
  <span style="color:{LML_GREY};font-size:0.82rem">= ln α · δt</span>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_plot:
        fig, ax = plt.subplots(figsize=(8.0, 3.6))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(T, ln_x, color=PATH_COLOR, lw=2.8)

        y_bot, y_top = draw_window_annotation(
            ax, t0, WIN_WIDTH, ln_x0, ln_x1,
            y_floor=min(0.0, float(ln_x.min())),
            y_max_val=float(ln_x.max()),
            color=PATH_COLOR,
            delta_label=f"δ(ln x) = {delta_ln_x:.2f}",
        )

        ax.set_xlim(-0.2, T_MAX + 1.5)
        ax.set_ylim(y_bot, y_top)
        ax.set_xlabel("time  t", fontsize=10, color=LML_BLUE)
        ax.set_ylabel("ln(x(t))", fontsize=10, color=LML_BLUE)
        ax.set_title(
            "ln x(t) = ln α · t + ln x(0)    (log-clock domain)",
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
