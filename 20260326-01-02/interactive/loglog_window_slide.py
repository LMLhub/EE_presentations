"""Slide 5tris: ln(ln(x)) gives constant increments for power-law dynamics.

x(t) = x(0)^(α^t)  →  ln(ln(x(t))) = t·ln(α) + ln(ln(x(0)))

This is a straight line — the double-log clock ticks evenly.
A sliding window confirms that δ(ln ln x) is constant everywhere.
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

ALPHA = 1.20    # > 1 — same as in power_law_worlds_slide
LN_X0 = 1.0    # ln(x(0))

T_MAX = 5.0
N_PTS = 400
T = np.linspace(0, T_MAX, N_PTS)

WIN_WIDTH = 2.0

# ln(ln(x(t))) = t·ln(α) + ln(ln(x(0)))
# For ln(x(0)) = LN_X0, ln(ln(x(0))) = ln(LN_X0).
# When LN_X0 = 1: ln(1) = 0, so  ln(ln(x(t))) = t·ln(α)
LN_ALPHA = np.log(ALPHA)
LLNX = LN_ALPHA * T + np.log(LN_X0)   # = LN_ALPHA * T when LN_X0 = 1

PATH_COLOR = FERMAT   # green — the "correct" ergodic transform


def loglog_window_slide() -> None:
    render_slide_header("Apply ln(ln(x)) — now the clock ticks steadily")

    t0 = st.slider(
        "← Shift measurement window →",
        min_value=0.0,
        max_value=T_MAX - WIN_WIDTH,
        value=2.0,
        step=0.1,
        key="ll_t0",
    )

    v0 = float(np.interp(t0, T, LLNX))
    v1 = float(np.interp(t0 + WIN_WIDTH, T, LLNX))
    delta_ll = v1 - v0  # always = LN_ALPHA * WIN_WIDTH

    col_formula, col_plot = st.columns([2.8, 6.2])

    with col_formula:
        st.markdown(
            f"""
<div style="background:{PANEL_BG};border:1px solid {PANEL_BORDER};
  border-left:6px solid {PATH_COLOR};border-radius:0.4rem;
  padding:0.9rem 1rem;margin-top:0.4rem">
  <b style="color:{PATH_COLOR}">Power-law dynamic — double-log clock</b><br><br>
  <span style="font-family:monospace">x(t+1) = x(t)<sup>α</sup></span><br>
  <span style="font-family:monospace">x(t) &nbsp;= x(0)<sup>(α<sup>t</sup>)</sup></span><br>
  <span style="font-family:monospace">ln ln x(t) = t·ln α + ln ln x(0)</span><br>
  <br>
  <span style="color:{LML_GREY};font-size:0.85rem">
    Window: t = {t0:.1f} → {t0 + WIN_WIDTH:.1f}<br>
    δt = {WIN_WIDTH:.1f}
  </span><br><br>
  <b style="color:{PATH_COLOR};font-size:1.15rem">δ(ln ln x) = {delta_ll:.3f}</b><br>
  <span style="color:{LML_GREY};font-size:0.82rem">= ln α · δt</span>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_plot:
        fig, ax = plt.subplots(figsize=(8.0, 3.6))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(T, LLNX, color=PATH_COLOR, lw=2.8)

        y_bot, y_top = draw_window_annotation(
            ax, t0, WIN_WIDTH, v0, v1,
            y_floor=min(0.0, float(LLNX.min())),
            y_max_val=float(LLNX.max()),
            color=PATH_COLOR,
            delta_label=f"δ(ln ln x) = {delta_ll:.3f}",
        )

        ax.set_xlim(-0.2, T_MAX + 1.5)
        ax.set_ylim(y_bot, y_top)
        ax.set_xlabel("time  t", fontsize=10, color=LML_BLUE)
        ax.set_ylabel("ln(ln(x(t)))", fontsize=10, color=LML_BLUE)
        ax.set_title(
            "ln ln x(t) = ln α · t + ln ln x(0)    (double-log clock)",
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
