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


APP_SLIDES: dict = {
    "demo": app_slide_demo,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
SLIDES: list = [
    ("pdf", 0),         # title page
    ("app", "demo"),    # interactive sine-wave demo
    ("pdf", 1),         # wealth vs. time figure
    ("pdf", 2),         # thank you / Galton board
]
