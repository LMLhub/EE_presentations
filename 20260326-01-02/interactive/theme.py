"""Shared EE house-style helpers for interactive Streamlit slides."""

import base64
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
LOGO_MARK = ROOT_DIR / "EE_presentations-Growth-Rates/shared/logos/logo_only.jpg"
LOGO_FULL = ROOT_DIR / "EE_presentations-Growth-Rates/shared/logos/lml_LOGO_whiteBG.jpg"

LML_BLUE = "#00466E"
LML_GREY = "#8E8E8E"
FERMAT = "#329632"
BERNOULLI = "#C83232"
PANEL_BG = "#F6F7F8"
PANEL_BORDER = "#D5D9DD"
TEXT_DARK = "#111111"
SLATE = "#6F7C86"


def inject_house_css() -> None:
    """Inject the shared CSS once per Streamlit session."""
    if st.session_state.get("_ee_house_css"):
        return

    st.session_state["_ee_house_css"] = True
    st.markdown(
        f"""
<style>
  .ee-kicker {{
    color: {LML_GREY};
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-size: 0.76rem;
    font-weight: 700;
    margin: 0 0 0.2rem 0;
  }}
  .ee-title {{
    color: {LML_BLUE};
    font-size: 1.95rem;
    line-height: 1.12;
    font-weight: 700;
    margin: 0;
  }}
  .ee-subtitle {{
    color: {TEXT_DARK};
    font-size: 1rem;
    line-height: 1.35;
    margin: 0.35rem 0 0 0;
  }}
  .ee-divider {{
    height: 3px;
    border-radius: 999px;
    margin: 0.45rem 0 1rem 0;
    background: linear-gradient(90deg, {LML_BLUE} 0%, {LML_BLUE} 42%, {LML_GREY} 42%, {LML_GREY} 100%);
  }}
  .ee-panel {{
    background: {PANEL_BG};
    border: 1px solid {PANEL_BORDER};
    border-left: 6px solid {LML_BLUE};
    border-radius: 0.4rem;
    padding: 0.75rem 0.95rem;
    margin: 0.15rem 0 0.9rem;
  }}
  .ee-panel--red {{
    border-left-color: {BERNOULLI};
  }}
  .ee-panel--green {{
    border-left-color: {FERMAT};
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


def render_header(title: str, subtitle: str | None = None) -> None:
    """Render a shared EE-branded heading row for app slides."""
    inject_house_css()

    col_title, col_logo = st.columns([7, 2])
    with col_title:
        st.markdown("<div class='ee-kicker'>Ergodicity Economics</div>", unsafe_allow_html=True)
        st.markdown(f"<h1 class='ee-title'>{title}</h1>", unsafe_allow_html=True)
        if subtitle:
            st.markdown(f"<p class='ee-subtitle'>{subtitle}</p>", unsafe_allow_html=True)
    with col_logo:
        st.image(str(LOGO_FULL), use_container_width=True)

    st.markdown("<div class='ee-divider'></div>", unsafe_allow_html=True)


def draw_window_annotation(
    ax,
    t0: float,
    win_width: float,
    v0: float,
    v1: float,
    y_floor: float,
    y_max_val: float,
    color: str,
    delta_label: str,
    dt_label: str = "δt",
    dt_row: int = 0,
) -> tuple[float, float]:
    """Draw a standardised measurement-window annotation on *ax*.

    Draws:
    • Two filled dots on the curve at (t0, v0) and (t0+win_width, v1).
    • A horizontal ↔ arrow below the data for δt.
    • A vertical ↕ arrow to the right of the window for δ(value).

    Parameters
    ----------
    y_floor   : bottom of the data region, typically ``min(0, path.min())``.
    y_max_val : maximum value of the plotted path.
    delta_label : label for the vertical arrow, e.g. ``"δx = 1.50"``.
    dt_label  : label for the horizontal arrow; defaults to ``"δt"``.
    dt_row    : row index (0, 1, 2, …) to stagger multiple δt arrows
                vertically so they don't overlap.

    Returns
    -------
    (y_bot, y_top) suitable for ``ax.set_ylim``.
    """
    y_range = max(y_max_val - y_floor, 1e-6)

    # Minimum arrow body = 20 % of the y-range so arrowheads never overlap.
    MIN_FRAC = 0.20
    mid = (v0 + v1) / 2.0
    half = max(abs(v1 - v0) / 2.0, y_range * MIN_FRAC / 2.0)
    v_lo = mid - half
    v_hi = mid + half

    ARROW = dict(arrowstyle="<->", color=color, lw=2.1, mutation_scale=10)

    # ── Dots at the true data positions on the curve ─────────────────────────
    ax.plot(t0,             v0, "o", color=color, ms=7, zorder=5)
    ax.plot(t0 + win_width, v1, "o", color=color, ms=7, zorder=5)

    # ── Horizontal δt arrow (below the data floor, staggered by dt_row) ──────
    ROW_STEP = 0.18   # fraction of y_range per row
    y_dt = y_floor - (0.10 + dt_row * ROW_STEP) * y_range
    ax.annotate("", xy=(t0 + win_width, y_dt), xytext=(t0, y_dt),
                arrowprops=ARROW)
    ax.text(t0 + win_width / 2, y_dt - 0.06 * y_range,
            dt_label, ha="center", va="top", color=color, fontsize=9)

    # ── Vertical δ(value) arrow (right of window, padded to MIN_FRAC) ────────
    x_arr = t0 + win_width + 0.35
    ax.annotate("", xy=(x_arr, v_hi), xytext=(x_arr, v_lo),
                arrowprops=ARROW)
    ax.text(x_arr + 0.20, mid,
            delta_label, va="center", color=color, fontsize=9.5,
            fontweight="bold")

    n_rows = dt_row + 1
    return (y_floor - (0.10 + n_rows * ROW_STEP + 0.08) * y_range,
            y_max_val + 0.10 * y_range)


def inject_slide_frame_css() -> None:
    """Inject the fixed blue sidebar + compact-layout CSS on every render.

    Calling this at the start of each app slide makes the content appear
    inside a beamer-style frame: LML-blue left bar with logo, white content
    area, no extra Streamlit padding.
    """
    logo_b64 = base64.b64encode(LOGO_MARK.read_bytes()).decode()

    st.markdown(
        f"""
<style>
  /* Push the entire main area to the right of the sidebar */
  .main, section[data-testid="stMain"] {{
    padding-left: 78px !important;
  }}
  /* Override presentation.py block-container padding */
  .main .block-container {{
    padding: 0.35rem 1.4rem 0.1rem 0.7rem !important;
    max-width: 100% !important;
  }}
  /* Tighter widget spacing */
  div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {{
    gap: 0.15rem !important;
  }}
  .stSlider {{ margin-top: 0.1rem !important; margin-bottom: 0.1rem !important; }}
</style>
<div id="ee-slide-bar" style="
    position:fixed; left:0; top:0; bottom:0; width:74px;
    background:{LML_BLUE}; z-index:10000;
    display:flex; flex-direction:column; align-items:center; padding-top:12px;
">
  <img src="data:image/jpeg;base64,{logo_b64}"
       style="width:54px; border-radius:3px; display:block;">
</div>
""",
        unsafe_allow_html=True,
    )


def render_slide_header(title: str) -> None:
    """Render a beamer-style frame title inside an app slide.

    Calls inject_slide_frame_css() automatically, so slides only need
    one call at the top of their render function.
    """
    inject_slide_frame_css()
    st.markdown(
        f"<h2 style='color:{LML_BLUE};font-weight:700;"
        f"font-size:1.4rem;line-height:1.1;margin:0 0 0.12rem 0'>{title}</h2>"
        f"<div style='height:3px;"
        f"background:linear-gradient(90deg,{LML_BLUE} 0%,{LML_BLUE} 42%,"
        f"{LML_GREY} 42%,{LML_GREY} 100%);margin-bottom:0.45rem'></div>",
        unsafe_allow_html=True,
    )


def render_panel(body_html: str, tone: str = "blue") -> None:
    """Render a simple house-style callout panel."""
    tone_class = ""
    if tone == "red":
        tone_class = " ee-panel--red"
    elif tone == "green":
        tone_class = " ee-panel--green"

    st.markdown(
        f"<div class='ee-panel{tone_class}'>{body_html}</div>",
        unsafe_allow_html=True,
    )
