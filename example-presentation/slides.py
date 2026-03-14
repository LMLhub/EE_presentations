"""
Slide deck definition for the example presentation.

APP_SLIDES maps keys to interactive Streamlit slide functions.
SLIDES defines the ordering of PDF pages and app slides.
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# App slide functions
# ---------------------------------------------------------------------------
def app_slide_brownian() -> None:
    """Interactive Brownian motion with adjustable drift and variance."""
    st.subheader("Brownian Motion with Drift")

    col1, col2, col3 = st.columns(3)
    with col1:
        mu = st.slider("Drift (μ)", -2.0, 2.0, 0.5, 0.1)
    with col2:
        sigma = st.slider("Volatility (σ)", 0.1, 3.0, 1.0, 0.1)
    with col3:
        n_paths = st.slider("Paths", 1, 50, 10, 1)

    n_steps = 500
    dt = 0.01
    t = np.linspace(0, n_steps * dt, n_steps)

    np.random.seed(42)

    fig, ax = plt.subplots(figsize=(9, 4))
    all_paths = np.zeros((n_paths, n_steps))
    for i in range(n_paths):
        increments = mu * dt + sigma * np.sqrt(dt) * np.random.randn(n_steps)
        all_paths[i] = np.cumsum(increments)
        ax.plot(t, all_paths[i], alpha=0.4, lw=0.8)

    # Ensemble mean
    if n_paths > 1:
        ensemble_mean = np.mean(all_paths, axis=0)
        ax.plot(t, ensemble_mean, color="black", lw=2.5, label="Ensemble mean")

    # Theoretical expectation
    ax.plot(t, mu * t, color="red", lw=2, ls="--", label=rf"$\mu t = {mu:.1f}\,t$")

    ax.set_xlabel("Time, $t$")
    ax.set_ylabel("$x(t)$")
    ax.set_title(rf"$dx = {mu:.1f}\,dt + {sigma:.1f}\,dW$")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)


APP_SLIDES: dict = {
    "brownian": app_slide_brownian,
}


# ---------------------------------------------------------------------------
# Slide ordering — each entry is ("pdf", page_index) or ("app", key)
# ---------------------------------------------------------------------------
def pdf_pages(spec) -> list[tuple[str, int]]:
    """Expand a PDF page spec into a list of ("pdf", index) tuples.

    spec can be:
      - an int          -> single page, e.g. pdf_pages(0)
      - a "start-end"   -> inclusive range, e.g. pdf_pages("0-4")
      - a list mixing the above, e.g. pdf_pages([0, "3-5", 8])
    Page indices are 0-based.
    """
    if isinstance(spec, list):
        result = []
        for item in spec:
            result.extend(pdf_pages(item))
        return result
    if isinstance(spec, str) and "-" in spec:
        start, end = spec.split("-")
        return [("pdf", i) for i in range(int(start), int(end) + 1)]
    return [("pdf", int(spec))]


SLIDES: list = [
    *pdf_pages("0-3"),          # title page … key observations
    ("app", "brownian"),        # interactive Brownian motion
    *pdf_pages(4),              # thank you
]
