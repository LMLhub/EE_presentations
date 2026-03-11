"""
Slide deck definition for presentation 20260326-01-02.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import base64
import io
import math
from pathlib import Path

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from PIL import Image

PDF_PATH = Path(__file__).parent / "main.pdf"

LML_BLUE = "#00466E"
LML_GREY = "#8E8E8E"
FERMAT = "#329632"
BERNOULLI = "#C83232"
SLATE = "#6F7C86"
GREY = "#6E6E6E"

# ---------------------------------------------------------------------------
# Shared CSS helpers
# ---------------------------------------------------------------------------
def inject_house_css() -> None:
    """Inject the minimal CSS used by the live app slides."""
    if st.session_state.get("_ee_house_css"):
        return

    st.session_state["_ee_house_css"] = True
    st.markdown(
        f"""
<style>
  .ee-title {{
    color: {LML_BLUE};
    font-size: 1.75rem;
    line-height: 1.12;
    font-weight: 700;
    margin: 0;
  }}
  .ee-divider {{
    height: 3px;
    border-radius: 999px;
    margin: 0.15rem 0 0.8rem 0;
    background: linear-gradient(90deg, {LML_BLUE} 0%, {LML_BLUE} 42%, {LML_GREY} 42%, {LML_GREY} 100%);
  }}
  .ee-note {{
    color: #6B7280;
    font-size: 0.84rem;
    line-height: 1.4;
  }}
  .ee-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.84rem;
  }}
  .ee-table th {{
    text-align: right;
    padding: 0.28rem 0.3rem;
    border-bottom: 2px solid {LML_BLUE};
  }}
  .ee-table th:first-child,
  .ee-table td:first-child {{
    text-align: left;
  }}
  .ee-table td {{
    padding: 0.26rem 0.3rem;
    border-bottom: 1px solid #E5E7EB;
  }}
</style>
""",
        unsafe_allow_html=True,
    )


def _centered_html(html: str) -> None:
    """Render HTML in the same centered width as the PDF slides."""
    _, col, _ = st.columns([0.3, 9.4, 0.3])
    with col:
        st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Clock slide helpers
# ---------------------------------------------------------------------------
CLOCK_SLIDE_IDX = 2
CLOCK_FRAMES = 72
CLOCK_FPS = 18
CLOCK_T_END = 4.0

LEFT_L = 28.63
LEFT_T = 84.31
LEFT_W = 9.03
LEFT_H = 15.29

RIGHT_L = 66.30
RIGHT_T = 84.31
RIGHT_W = 19.38
RIGHT_H = 15.29


def _draw_clock(ax, cx: float, cy: float, r: float, angle_deg: float, color: str) -> None:
    """Draw one clock without labels so the slide text comes from the PDF."""
    ax.add_patch(plt.Circle((cx, cy), r, color=color, fill=False, lw=2.4, zorder=2))

    for hour in range(12):
        angle = math.radians(hour * 30)
        ax.plot(
            [cx + 0.88 * r * math.sin(angle), cx + r * math.sin(angle)],
            [cy + 0.88 * r * math.cos(angle), cy + r * math.cos(angle)],
            color=color,
            lw=1.05,
            alpha=0.58,
            zorder=3,
        )

    hand_r = 0.72 * r
    rad = math.radians(angle_deg)
    hx = cx + hand_r * math.sin(rad)
    hy = cy + hand_r * math.cos(rad)
    ax.plot([cx, hx], [cy, hy], color=color, lw=2.5, zorder=4, solid_capstyle="round")
    ax.add_patch(plt.Circle((hx, hy), 0.11 * r, color=color, zorder=5))
    ax.add_patch(plt.Circle((cx, cy), 0.05 * r, color=GREY, zorder=6))


def _blank_ax(ax, xlim: tuple[float, float], ylim: tuple[float, float]) -> None:
    ax.set_facecolor("white")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])


def _render_left_frame(angle_deg: float) -> Image.Image:
    """Render one additive clock frame at high resolution."""
    fig, ax = plt.subplots(figsize=(2.2, 2.2))
    fig.patch.set_facecolor("white")
    _blank_ax(ax, (-1.08, 1.08), (-1.08, 1.08))
    _draw_clock(ax, 0.0, 0.0, 1.0, angle_deg, FERMAT)

    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=220,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="white",
    )
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("P", palette=Image.ADAPTIVE)


def _render_right_frame(log_angle: float, lin_angle: float) -> Image.Image:
    """Render one multiplicative clock frame at high resolution."""
    fig, ax = plt.subplots(figsize=(4.8, 2.2))
    fig.patch.set_facecolor("white")
    _blank_ax(ax, (-2.35, 2.35), (-1.08, 1.08))
    _draw_clock(ax, -1.2, 0.0, 1.0, lin_angle, BERNOULLI)
    _draw_clock(ax, 1.2, 0.0, 1.0, log_angle, LML_BLUE)

    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=220,
        bbox_inches="tight",
        pad_inches=0,
        facecolor="white",
    )
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("P", palette=Image.ADAPTIVE)


@st.cache_data(show_spinner=False)
def _clock_left_gif() -> bytes:
    """Build the additive clock animation."""
    frames: list[Image.Image] = []
    for i in range(CLOCK_FRAMES):
        t = (i / CLOCK_FRAMES) * CLOCK_T_END
        angle = (360.0 * t / CLOCK_T_END) % 360
        frames.append(_render_left_frame(angle))

    gif_buf = io.BytesIO()
    frames[0].save(
        gif_buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=int(1000 / CLOCK_FPS),
        optimize=False,
    )
    return gif_buf.getvalue()


@st.cache_data(show_spinner=False)
def _clock_right_gif() -> bytes:
    """Build the multiplicative clock animation."""
    frames: list[Image.Image] = []
    for i in range(CLOCK_FRAMES):
        t = (i / CLOCK_FRAMES) * CLOCK_T_END
        log_angle = (360.0 * t / CLOCK_T_END) % 360
        lin_angle = (
            360.0 * (math.exp(1.8 * t) - 1.0) / (math.exp(1.8 * CLOCK_T_END) - 1.0) * 4.0
        ) % 360
        frames.append(_render_right_frame(log_angle, lin_angle))

    gif_buf = io.BytesIO()
    frames[0].save(
        gif_buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=int(1000 / CLOCK_FPS),
        optimize=False,
    )
    return gif_buf.getvalue()


@st.cache_data(show_spinner=False)
def _clock_background_png() -> bytes:
    """Render slide 3 from the compiled PDF at high resolution."""
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    doc = fitz.open(PDF_PATH)
    if doc.page_count <= CLOCK_SLIDE_IDX:
        doc.close()
        raise IndexError(f"main.pdf has only {doc.page_count} pages")

    page = doc[CLOCK_SLIDE_IDX]
    pix = page.get_pixmap(matrix=fitz.Matrix(4.0, 4.0))
    png = pix.tobytes("png")
    doc.close()
    return png


def _b64(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def app_slide_clock() -> None:
    """Render slide 3 with only the clocks animated, keeping the PDF crisp."""
    try:
        with st.spinner("Loading slide..."):
            bg_png = _clock_background_png()
            gif_left = _clock_left_gif()
            gif_right = _clock_right_gif()
    except (FileNotFoundError, IndexError) as exc:
        st.error(str(exc))
        st.info("Compile main.tex first so the app can overlay the animated clocks on slide 3.")
        return

    bg_uri = _b64(bg_png, "image/png")
    gif_left_uri = _b64(gif_left, "image/gif")
    gif_right_uri = _b64(gif_right, "image/gif")

    _centered_html(
        f"""
<div style="position:relative; display:block; width:100%; line-height:0">
  <img src="{bg_uri}" style="width:100%; height:auto; display:block;">
  <img
    src="{gif_left_uri}"
    style="
      position:absolute;
      left:{LEFT_L:.2f}%;
      top:{LEFT_T:.2f}%;
      width:{LEFT_W:.2f}%;
      height:{LEFT_H:.2f}%;
      object-fit:fill;
    "
  >
  <img
    src="{gif_right_uri}"
    style="
      position:absolute;
      left:{RIGHT_L:.2f}%;
      top:{RIGHT_T:.2f}%;
      width:{RIGHT_W:.2f}%;
      height:{RIGHT_H:.2f}%;
      object-fit:fill;
    "
  >
</div>
"""
    )


# ---------------------------------------------------------------------------
# Window slide helpers
# ---------------------------------------------------------------------------
WINDOW_T_MAX = 20.0
WINDOW_N_PTS = 500
WINDOW_T = np.linspace(0, WINDOW_T_MAX, WINDOW_N_PTS)
WINDOW_GROWTH = [0.15, 0.02, 0.10]
WINDOW_PATHS = [np.exp(g * WINDOW_T) for g in WINDOW_GROWTH]
WINDOW_LABELS = ["Path 1", "Path 2", "Path 3"]
WINDOW_PATH_COLS = [LML_BLUE, LML_GREY, FERMAT]
WINDOW_COLS = [BERNOULLI, SLATE]


def _arith(path: np.ndarray, t_start: float, t_len: float) -> float:
    x0 = np.interp(t_start, WINDOW_T, path)
    x1 = np.interp(t_start + t_len, WINDOW_T, path)
    return (x1 - x0) / t_len if t_len > 0 else float("nan")


def _table_html(a_start: float, a_len: float, b_start: float, b_len: float) -> str:
    rows = []
    for path, label, color, growth in zip(WINDOW_PATHS, WINDOW_LABELS, WINDOW_PATH_COLS, WINDOW_GROWTH):
        rows.append(
            "<tr>"
            f"<td style='color:{color};font-weight:700'>{label}</td>"
            f"<td style='color:{WINDOW_COLS[0]}'>{_arith(path, a_start, a_len):.3f}</td>"
            f"<td style='color:{WINDOW_COLS[1]}'>{_arith(path, b_start, b_len):.3f}</td>"
            f"<td style='color:{LML_BLUE};font-weight:700'>{growth:.2f}</td>"
            "</tr>"
        )

    return f"""
<table class='ee-table'>
  <thead>
    <tr>
      <th>Path</th>
      <th style='color:{WINDOW_COLS[0]}'>Lin A</th>
      <th style='color:{WINDOW_COLS[1]}'>Lin B</th>
      <th style='color:{LML_BLUE}'>Log</th>
    </tr>
  </thead>
  <tbody>
    {''.join(rows)}
  </tbody>
</table>
"""


def app_slide_window() -> None:
    """Interactive measurement-window explorer."""
    inject_house_css()
    st.markdown(
        """
<h1 class='ee-title'>The wrong clock gives a different answer every time</h1>
<div class='ee-divider'></div>
""",
        unsafe_allow_html=True,
    )

    col_ctrl, col_chart = st.columns([3.2, 5.3])

    with col_ctrl:
        st.markdown(
            f"<p style='color:{WINDOW_COLS[0]};font-weight:700;margin:0'>Window A</p>",
            unsafe_allow_html=True,
        )
        a_start = st.slider("Start A", 0.0, WINDOW_T_MAX - 1.0, 2.0, 0.5, key="a_start")
        a_len = st.slider(
            "Length A",
            1.0,
            min(10.0, WINDOW_T_MAX - a_start),
            5.0,
            0.5,
            key="a_len",
        )
        st.markdown(
            f"<p class='ee-note' style='color:{WINDOW_COLS[0]};margin-top:-0.35rem'>"
            f"Window A measures t = {a_start:.1f} to {a_start + a_len:.1f}</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<p style='color:{WINDOW_COLS[1]};font-weight:700;margin:0'>Window B</p>",
            unsafe_allow_html=True,
        )
        b_start = st.slider("Start B", 0.0, WINDOW_T_MAX - 1.0, 12.0, 0.5, key="b_start")
        b_len = st.slider(
            "Length B",
            1.0,
            min(10.0, WINDOW_T_MAX - b_start),
            5.0,
            0.5,
            key="b_len",
        )
        st.markdown(
            f"<p class='ee-note' style='color:{WINDOW_COLS[1]};margin-top:-0.35rem'>"
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

        for path, color in zip(WINDOW_PATHS, WINDOW_PATH_COLS):
            ax.plot(WINDOW_T, path, color=color, lw=2.4)

        y_max = max(path.max() for path in WINDOW_PATHS)

        for start, length, color, name in [
            (a_start, a_len, WINDOW_COLS[0], "A"),
            (b_start, b_len, WINDOW_COLS[1], "B"),
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

        ax.set_xlim(0, WINDOW_T_MAX)
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
        for path, label, color, growth in zip(WINDOW_PATHS, WINDOW_LABELS, WINDOW_PATH_COLS, WINDOW_GROWTH):
            y_val = np.interp(label_x, WINDOW_T, path)
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


APP_SLIDES: dict = {
    "clock": app_slide_clock,
    "window": app_slide_window,
}


SLIDES: list = [
    ("pdf", 0),         # title page
    ("pdf", 1),         # misconception
    ("app", "clock"),   # animated clocks
    ("app", "window"),  # adjustable measurement windows
    ("pdf", 4),         # additive discounting
    ("pdf", 5),         # multiplicative discounting
    ("pdf", 6),         # bridge to other dynamics
    ("pdf", 7),         # power-law clock
    ("pdf", 8),         # absorbing boundaries
    ("pdf", 9),         # summary
]
