"""Animated clock overlay for slide 3 using a high-resolution PDF background."""

import base64
import io
import math
from pathlib import Path

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

FERMAT = "#329632"
BERNOULLI = "#C83232"
LML_BLUE = "#00466E"
GREY = "#6E6E6E"

PDF_PATH = Path(__file__).parent.parent / "presentation.pdf"
SLIDE_IDX = 2
N_FRAMES = 72
FPS = 18
T_END = 4.0

# Measured from the rendered PDF background of slide 3.
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
def _gif_left() -> bytes:
    """Build the additive clock animation."""
    frames: list[Image.Image] = []
    for i in range(N_FRAMES):
        t = (i / N_FRAMES) * T_END
        angle = (360.0 * t / T_END) % 360
        frames.append(_render_left_frame(angle))

    gif_buf = io.BytesIO()
    frames[0].save(
        gif_buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=int(1000 / FPS),
        optimize=False,
    )
    return gif_buf.getvalue()


@st.cache_data(show_spinner=False)
def _gif_right() -> bytes:
    """Build the multiplicative clock animation."""
    frames: list[Image.Image] = []
    for i in range(N_FRAMES):
        t = (i / N_FRAMES) * T_END
        log_angle = (360.0 * t / T_END) % 360
        lin_angle = (
            360.0 * (math.exp(1.8 * t) - 1.0) / (math.exp(1.8 * T_END) - 1.0) * 4.0
        ) % 360
        frames.append(_render_right_frame(log_angle, lin_angle))

    gif_buf = io.BytesIO()
    frames[0].save(
        gif_buf,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=int(1000 / FPS),
        optimize=False,
    )
    return gif_buf.getvalue()


@st.cache_data(show_spinner=False)
def _render_background() -> bytes:
    """Render slide 3 from the compiled PDF at high resolution."""
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF not found at {PDF_PATH}")

    doc = fitz.open(PDF_PATH)
    if doc.page_count <= SLIDE_IDX:
        doc.close()
        raise IndexError(f"presentation.pdf has only {doc.page_count} pages")

    page = doc[SLIDE_IDX]
    pix = page.get_pixmap(matrix=fitz.Matrix(4.0, 4.0))
    png = pix.tobytes("png")
    doc.close()
    return png


def _b64(data: bytes, mime: str) -> str:
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def clock_slide() -> None:
    """Render slide 3 with only the clocks animated, keeping the PDF crisp."""
    try:
        with st.spinner("Loading slide..."):
            bg_png = _render_background()
            gif_left = _gif_left()
            gif_right = _gif_right()
    except (FileNotFoundError, IndexError) as exc:
        st.error(str(exc))
        st.info("Compile presentation.tex first so the app can overlay the animated clocks on slide 3.")
        return

    bg_uri = _b64(bg_png, "image/png")
    gif_left_uri = _b64(gif_left, "image/gif")
    gif_right_uri = _b64(gif_right, "image/gif")

    _, img_col, _ = st.columns([0.3, 9.4, 0.3])
    with img_col:
        st.markdown(
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
""",
            unsafe_allow_html=True,
        )
