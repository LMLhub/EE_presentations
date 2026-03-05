"""
Streamlit presentation viewer.

Usage:
  streamlit run presentation.py -- presentations/20260326-01-01

Slide deck = PDF pages + inline Streamlit app slides interspersed.
Add new app slides by:
  1. Writing a function  def my_slide(): ...
  2. Adding it to APP_SLIDES dict with a unique key.
  3. Inserting ("app", "my_key") at the desired position in build_slides().
"""

import sys
import streamlit as st
import streamlit.components.v1 as components
import fitz  # PyMuPDF
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# Accept presentation folder as a CLI argument (after the -- separator)
if len(sys.argv) < 2:
    st.error("Usage: `streamlit run presentation.py -- <presentation-folder>`")
    st.stop()

PDF_PATH = Path(sys.argv[1]) / "main.pdf"


# ---------------------------------------------------------------------------
# PDF helpers
# ---------------------------------------------------------------------------
@st.cache_data
def get_pdf_page_count() -> int:
    doc = fitz.open(PDF_PATH)
    n = doc.page_count
    doc.close()
    return n


@st.cache_data
def render_pdf_page(page_index: int) -> str:
    """Render a single PDF page to an SVG string (true vector)."""
    doc = fitz.open(PDF_PATH)
    page = doc[page_index]
    svg = page.get_svg_image(matrix=fitz.Identity)
    doc.close()
    return svg


# ---------------------------------------------------------------------------
# Custom app slides — add your own here
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
# Slide deck definition
# ---------------------------------------------------------------------------
def build_slides() -> list[tuple[str, int | str]]:
    """
    Return an ordered list of (kind, value) pairs where:
      ("pdf", page_index)  — render page from the PDF (0-based index)
      ("app", key)         — call APP_SLIDES[key]()
    """
    n = get_pdf_page_count()
    mid = max(1, n // 2)

    slides: list[tuple[str, int | str]] = []

    # First half of PDF
    for i in range(mid):
        slides.append(("pdf", i))

    # Inline app slide
    slides.append(("app", "demo"))

    # Second half of PDF
    for i in range(mid, n):
        slides.append(("pdf", i))

    return slides


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------
CSS = """
<style>
.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
[data-testid="stMain"] {
    padding: 0 !important;
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
footer { display: none !important; }

/* Hide the navigation sidebar entirely — buttons stay in DOM for keyboard JS */
[data-testid="stSidebar"] {
    opacity: 0 !important;
    pointer-events: none !important;
    position: fixed !important;
    left: -200vw !important;
}
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarContent"] ~ button {
    display: none !important;
}
</style>
"""


def show_pdf_page(svg: str) -> None:
    """Display an SVG page filling the available viewport height."""
    # Apply height directly on the <svg> element — no wrapper div needed,
    # which avoids any stray closing tags from confusing the HTML parser.
    svg_scaled = svg.replace(
        "<svg ",
        '<svg style="'
        "height:calc(100vh - 4px);"
        "width:auto;"
        "max-width:100%;"
        "display:block;"
        'margin:0;" ',
        1,
    )
    st.markdown(svg_scaled, unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="Presentation", layout="wide", initial_sidebar_state="expanded")
    st.markdown(CSS, unsafe_allow_html=True)

    slides = build_slides()
    total = len(slides)

    if "slide_idx" not in st.session_state:
        st.session_state.slide_idx = 0

    # Keyboard navigation (arrow keys)
    components.html(
        """
        <script>
        window.parent.document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                for (const btn of window.parent.document.querySelectorAll('button')) {
                    if (btn.innerText.includes('Next')) { btn.click(); break; }
                }
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                for (const btn of window.parent.document.querySelectorAll('button')) {
                    if (btn.innerText.includes('Prev')) { btn.click(); break; }
                }
            }
        });
        </script>
        """,
        height=0,
    )

    idx: int = st.session_state.slide_idx
    kind, value = slides[idx]

    # Navigation buttons live in the sidebar — hidden off-screen via CSS,
    # but present in the DOM so the keyboard JS can click them.
    with st.sidebar:
        if st.button("◀ Prev", disabled=(idx == 0), use_container_width=True):
            st.session_state.slide_idx -= 1
            st.rerun()
        if st.button("Next ▶", disabled=(idx == total - 1), use_container_width=True):
            st.session_state.slide_idx += 1
            st.rerun()

    # Render current slide
    if kind == "pdf":
        svg = render_pdf_page(int(value))
        show_pdf_page(svg)
    elif kind == "app":
        APP_SLIDES[str(value)]()
    else:
        st.error(f"Unknown slide kind: {kind!r}")


if __name__ == "__main__":
    main()
