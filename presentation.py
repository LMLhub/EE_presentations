"""
Streamlit presentation viewer.

Usage:
  streamlit run presentation.py -- presentations/20260326-01-01

Renders a slide deck composed of PDF pages and interactive Streamlit app
slides.  Each presentation folder contains a slides.py that defines:
  - APP_SLIDES:  dict mapping keys to slide functions
  - build_slides(pdf_page_count):  returns the ordered slide list
"""

import sys
import importlib.util
import streamlit as st
import streamlit.components.v1 as components
import fitz  # PyMuPDF
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
# Accept presentation folder as a CLI argument (after the -- separator)
if len(sys.argv) < 2:
    st.error("Usage: `streamlit run presentation.py -- <presentation-folder>`")
    st.stop()

PRES_DIR = Path(sys.argv[1])
PDF_PATH = PRES_DIR / "main.pdf"


# ---------------------------------------------------------------------------
# Load presentation-specific slides.py
# ---------------------------------------------------------------------------
def _load_slides_module(pres_dir: Path):
    """Dynamically import slides.py from the presentation folder."""
    slides_file = pres_dir / "slides.py"
    if not slides_file.exists():
        st.error(f"No slides.py found in {pres_dir}")
        st.stop()
    spec = importlib.util.spec_from_file_location("slides", slides_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_slides_mod = _load_slides_module(PRES_DIR)
APP_SLIDES: dict = _slides_mod.APP_SLIDES
build_slides = _slides_mod.build_slides


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

    slides = build_slides(get_pdf_page_count())
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
