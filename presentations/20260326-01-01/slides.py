"""
Custom interactive app slides for this presentation.

Defines app-slide functions, the APP_SLIDES dict, and a custom
build_slides() that interleaves the demo slide at the midpoint
of the PDF deck.
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


# Map keys to app-slide functions
APP_SLIDES: dict = {
    "demo": app_slide_demo,
}


# ---------------------------------------------------------------------------
# Custom slide ordering — interleave the demo slide at the midpoint
# ---------------------------------------------------------------------------
def build_slides(pdf_page_count: int, app_slides: dict) -> list[tuple[str, int | str]]:
    """Insert the interactive demo slide halfway through the PDF pages."""
    n = pdf_page_count
    mid = max(1, n // 2)

    slides: list[tuple[str, int | str]] = []

    # First half of PDF pages
    for i in range(mid):
        slides.append(("pdf", i))

    # Inline app slide
    slides.append(("app", "demo"))

    # Second half of PDF pages
    for i in range(mid, n):
        slides.append(("pdf", i))

    return slides
