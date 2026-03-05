"""
Custom interactive app slides for this presentation.

Defines app-slide functions and the APP_SLIDES dict.
The shared presentation.py viewer handles combining these
with the PDF pages.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


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
