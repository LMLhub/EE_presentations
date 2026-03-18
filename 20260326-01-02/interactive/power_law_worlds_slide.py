"""Slide 5bis: Power-law dynamics fail in both x and ln(x) worlds.

x(t) = x(0)^(α^t).  Shown side by side:
  left panel:  x(t)      — super-exponential, δx varies wildly
  right panel: ln(x(t))  — still exponential,  δ(ln x) also varies

A single shared slider moves both windows simultaneously, making clear
that neither the additive nor the multiplicative clock gives constant growth.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import (
    LML_BLUE, LML_GREY, BERNOULLI, render_slide_header, draw_window_annotation,
)

# Power-law parameters: x(t) = exp(LN_X0 · ALPHA^t)
ALPHA = 1.20    # > 1
LN_X0 = 1.0     # ln(x(0)) = 1, so x(0) = e

T_MAX = 5.0
N_PTS = 400
T = np.linspace(0, T_MAX, N_PTS)

WIN_WIDTH = 2.0

# Derived paths
LN_X = LN_X0 * ALPHA ** T          # ln(x(t))
X_PATH = np.exp(LN_X)              # x(t)

PATH_COLOR = BERNOULLI  # red — "wrong" worlds


def _delta_str(arr: np.ndarray, t0: float) -> str:
    v0 = float(np.interp(t0, T, arr))
    v1 = float(np.interp(t0 + WIN_WIDTH, T, arr))
    return f"{v1 - v0:.3f}"


def power_law_worlds_slide() -> None:
    render_slide_header("Power-law dynamics: neither x nor ln(x) gives constant increments")

    t0 = st.slider(
        "← Shift measurement window →",
        min_value=0.0,
        max_value=T_MAX - WIN_WIDTH,
        value=1.0,
        step=0.1,
        key="pl_t0",
    )

    dx_str = _delta_str(X_PATH, t0)
    dlnx_str = _delta_str(LN_X, t0)

    # ── Two-panel plot ────────────────────────────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.6))
    fig.patch.set_facecolor("white")

    panel_data = [
        (axes[0], X_PATH,  "x(t)",      f"δx = {dx_str}",     "wealth  x(t)"),
        (axes[1], LN_X,    "ln(x(t))", f"δ(ln x) = {dlnx_str}", "ln(x(t))"),
    ]

    for ax, path, title_suffix, delta_label, ylabel in panel_data:
        ax.set_facecolor("white")
        ax.plot(T, path, color=PATH_COLOR, lw=2.6)

        v0 = float(np.interp(t0, T, path))
        v1 = float(np.interp(t0 + WIN_WIDTH, T, path))

        y_bot, y_top = draw_window_annotation(
            ax, t0, WIN_WIDTH, v0, v1,
            y_floor=min(0.0, float(path.min())),
            y_max_val=float(path.max()),
            color=BERNOULLI,
            delta_label=delta_label,
        )

        ax.set_xlim(-0.1, T_MAX + 1.5)
        ax.set_ylim(y_bot, y_top)
        ax.set_xlabel("time  t", fontsize=9.5, color=LML_BLUE)
        ax.set_ylabel(ylabel, fontsize=9.5, color=LML_BLUE)
        ax.set_title(title_suffix, fontsize=10.5, color=LML_BLUE, fontweight="bold")
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines["left"].set_color("#9CA3AF")
        ax.spines["bottom"].set_color("#9CA3AF")
        ax.tick_params(colors="#374151")
        ax.grid(axis="x", color="#E5E7EB", lw=0.8)

    fig.suptitle(
        "x(t) = x(0)^(α^t)    (power-law dynamic)",
        fontsize=11, color=LML_BLUE, fontweight="bold", y=1.01,
    )
    plt.tight_layout(pad=0.7)

    _, img_col, _ = st.columns([0.3, 9.4, 0.3])
    with img_col:
        st.pyplot(fig, use_container_width=True)
    plt.close(fig)

