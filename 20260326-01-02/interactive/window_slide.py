"""Interactive measurement-window slide styled to match the EE presentation theme."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from interactive.theme import BERNOULLI, FERMAT, LML_BLUE, LML_GREY, SLATE, inject_house_css

PATH_COLS = [LML_BLUE, LML_GREY, FERMAT]
WIN_COLS = [BERNOULLI, SLATE]
T_MAX = 20.0
N_PTS = 500
T = np.linspace(0, T_MAX, N_PTS)
GROWTH = [0.15, 0.02, 0.10]
PATHS = [np.exp(g * T) for g in GROWTH]
LABELS = ["Path 1", "Path 2", "Path 3"]


def _arith(path: np.ndarray, t_start: float, t_len: float) -> float:
    x0 = np.interp(t_start, T, path)
    x1 = np.interp(t_start + t_len, T, path)
    return (x1 - x0) / t_len if t_len > 0 else float("nan")


def _table_html(a_start: float, a_len: float, b_start: float, b_len: float) -> str:
    rows = []
    for path, label, color, growth in zip(PATHS, LABELS, PATH_COLS, GROWTH):
        rows.append(
            "<tr>"
            f"<td style='color:{color};font-weight:700'>{label}</td>"
            f"<td style='color:{WIN_COLS[0]}'>{_arith(path, a_start, a_len):.3f}</td>"
            f"<td style='color:{WIN_COLS[1]}'>{_arith(path, b_start, b_len):.3f}</td>"
            f"<td style='color:{LML_BLUE};font-weight:700'>{growth:.2f}</td>"
            "</tr>"
        )

    return f"""
<table class='ee-table'>
  <thead>
    <tr>
      <th>Path</th>
      <th style='color:{WIN_COLS[0]}'>Lin A</th>
      <th style='color:{WIN_COLS[1]}'>Lin B</th>
      <th style='color:{LML_BLUE}'>Log</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>
"""


def window_slide() -> None:
    """Render the house-styled measurement-window explorer."""
    inject_house_css()
    st.markdown(
        f"""
<h1 class='ee-title' style='font-size:1.75rem;margin-bottom:0.2rem'>
  The wrong clock gives a different answer every time
</h1>
<div class='ee-divider' style='margin-top:0;margin-bottom:0.8rem'></div>
""",
        unsafe_allow_html=True,
    )

    col_ctrl, col_chart = st.columns([3.2, 5.3])

    with col_ctrl:
        st.markdown(f"<p style='color:{WIN_COLS[0]};font-weight:700;margin:0'>Window A</p>", unsafe_allow_html=True)
        a_start = st.slider("Start A", 0.0, T_MAX - 1.0, 2.0, 0.5, key="a_start")
        a_len = st.slider(
            "Length A",
            1.0,
            min(10.0, T_MAX - a_start),
            5.0,
            0.5,
            key="a_len",
        )
        st.markdown(
            f"<p class='ee-note' style='color:{WIN_COLS[0]};margin-top:-0.35rem'>"
            f"Window A measures t = {a_start:.1f} to {a_start + a_len:.1f}</p>",
            unsafe_allow_html=True,
        )

        st.markdown(f"<p style='color:{WIN_COLS[1]};font-weight:700;margin:0'>Window B</p>", unsafe_allow_html=True)
        b_start = st.slider("Start B", 0.0, T_MAX - 1.0, 12.0, 0.5, key="b_start")
        b_len = st.slider(
            "Length B",
            1.0,
            min(10.0, T_MAX - b_start),
            5.0,
            0.5,
            key="b_len",
        )
        st.markdown(
            f"<p class='ee-note' style='color:{WIN_COLS[1]};margin-top:-0.35rem'>"
            f"Window B measures t = {b_start:.1f} to {b_start + b_len:.1f}</p>",
            unsafe_allow_html=True,
        )

        st.markdown(_table_html(a_start, a_len, b_start, b_len), unsafe_allow_html=True)
        st.markdown(
            "<p class='ee-note'>Linear clock: (x<sub>1</sub> - x<sub>0</sub>) / &Delta;t. "
            "Log clock: &Delta;ln x / &Delta;t = g.</p>",
            unsafe_allow_html=True,
        )

    with col_chart:
        fig, ax = plt.subplots(figsize=(7.2, 4.5))
        fig.patch.set_facecolor("white")
        ax.set_facecolor("white")

        for path, label, color, growth in zip(PATHS, LABELS, PATH_COLS, GROWTH):
            ax.plot(T, path, color=color, lw=2.4)

        y_max = max(path.max() for path in PATHS)

        for start, length, color, name in [
            (a_start, a_len, WIN_COLS[0], "A"),
            (b_start, b_len, WIN_COLS[1], "B"),
        ]:
            rect = patches.Rectangle(
                (start, 0.0),
                length,
                y_max * 1.08,
                linewidth=2,
                edgecolor=color,
                facecolor=color + "22",
                zorder=3,
            )
            ax.add_patch(rect)
            ax.text(
                start + length / 2.0,
                y_max * 1.02,
                f"Window {name}",
                ha="center",
                va="bottom",
                color=color,
                fontsize=9.5,
                fontweight="bold",
            )

        ax.set_xlim(0, T_MAX)
        ax.set_ylim(0, y_max * 1.15)
        ax.set_xlabel("time  t", fontsize=10, color=LML_BLUE)
        ax.set_ylabel("wealth  x(t)", fontsize=10, color=LML_BLUE)
        ax.set_title("Three paths, same log growth rate", fontsize=11, color=LML_BLUE, fontweight="bold")
        ax.grid(axis="x", color="#E5E7EB", linewidth=0.8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines["left"].set_color("#9CA3AF")
        ax.spines["bottom"].set_color("#9CA3AF")
        ax.tick_params(colors="#374151")

        label_x = 16.6
        for path, label, color, growth in zip(PATHS, LABELS, PATH_COLS, GROWTH):
            y_val = np.interp(label_x, T, path)
            ax.text(
                label_x,
                y_val,
                f"{label}  (g={growth:.2f})",
                color=color,
                fontsize=8.8,
                fontweight="bold",
                va="center",
                ha="left",
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 1.8},
            )

        plt.tight_layout(pad=0.6)

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    st.markdown(
        "<p class='ee-note'>If your clock is wrong, the estimated growth rate depends on where and when you measure.</p>",
        unsafe_allow_html=True,
    )
