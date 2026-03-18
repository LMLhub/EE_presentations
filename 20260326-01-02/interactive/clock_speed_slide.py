"""Slide 4bis: Variable clock speed for multiplicative dynamics.

First proposed fix: if you want a constant δx from a multiplicative path,
you must shrink the measurement window (clock rotation) as wealth grows.
Three anchors on the curve show how the required δt shrinks at higher wealth.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import (
    LML_BLUE, LML_GREY, BERNOULLI, FERMAT, PANEL_BG, PANEL_BORDER,
    render_slide_header, draw_window_annotation,
)

T_MAX = 8.0
N_PTS = 400
T = np.linspace(0, T_MAX, N_PTS)

G = 0.30          # log-growth rate
X0 = 1.0
TARGET_DX = 1.0   # the δx we want to achieve at each anchor

# Three starting positions — spaced so windows don't overlap in x
ANCHORS = [1.0, 3.5, 5.5]
WIN_COLORS = [FERMAT, LML_BLUE, BERNOULLI]


def _dt_for_target(x_anchor: float) -> float:
    """Return Δt needed so x(t0+Δt) - x(t0) = TARGET_DX, given x(t0) = x_anchor."""
    return float(np.log(1.0 + TARGET_DX / x_anchor) / G)


def clock_speed_slide() -> None:
    render_slide_header("Solution 1: speed up the clock as wealth grows")

    x = X0 * np.exp(G * T)

    # Pre-compute anchor data
    anchor_data = []
    for t_anchor, color in zip(ANCHORS, WIN_COLORS):
        x_anchor = X0 * np.exp(G * t_anchor)
        dt_ = _dt_for_target(x_anchor)
        x_end = x_anchor + TARGET_DX
        anchor_data.append((t_anchor, x_anchor, dt_, x_end, color))

    col_text, col_plot = st.columns([2.8, 6.2])

    with col_text:
        table_rows = "".join(
            f"<tr>"
            f"<td>t = {t_a:.0f}</td>"
            f"<td style='color:{c}'>x ≈ {x_a:.1f}</td>"
            f"<td style='color:{c}'><b>δt = {dt_:.2f}</b></td>"
            f"</tr>"
            for t_a, x_a, dt_, _, c in anchor_data
        )

        st.markdown(
            f"""
<div style="background:{PANEL_BG};border:1px solid {PANEL_BORDER};
  border-left:6px solid {LML_BLUE};border-radius:0.4rem;
  padding:0.9rem 1rem;margin-top:0.4rem">
  <b style="color:{LML_BLUE}">Target: δx = {TARGET_DX:.0f} at every position</b><br><br>
  <table style="width:100%;font-size:0.85rem;border-collapse:collapse">
    <thead>
      <tr>
        <th style="text-align:left;border-bottom:2px solid {LML_BLUE};padding:0.2rem 0.3rem">
          Position</th>
        <th style="border-bottom:2px solid {LML_BLUE};padding:0.2rem 0.3rem">
          Wealth</th>
        <th style="border-bottom:2px solid {LML_BLUE};padding:0.2rem 0.3rem">
          Need δt</th>
      </tr>
    </thead>
    <tbody>
      {table_rows}
    </tbody>
  </table>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_plot:
        fig, ax = plt.subplots(figsize=(8.0, 3.6))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        ax.plot(T, x, color=LML_BLUE, lw=2.8)

        y_floor = 0.0
        y_max_val = float(x.max())
        y_bot = y_top = None

        for row, (t_anchor, x_anchor, dt_, x_end, color) in enumerate(anchor_data):
            y_bot, y_top = draw_window_annotation(
                ax, t_anchor, dt_, x_anchor, x_end,
                y_floor=y_floor, y_max_val=y_max_val,
                color=color,
                delta_label=f"δx = {TARGET_DX:.0f}",
                dt_label=f"δt = {dt_:.2f}",
                dt_row=row,
            )

        ax.set_xlim(-0.2, T_MAX + 1.5)
        ax.set_ylim(y_bot, y_top)
        ax.set_xlabel("time  t", fontsize=10, color=LML_BLUE)
        ax.set_ylabel("wealth  x(t)", fontsize=10, color=LML_BLUE)
        ax.set_title(
            "Same δx requires a shorter clock rotation at higher wealth",
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
