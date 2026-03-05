"""
Slide-deck definition for the example-figs presentation.

A PDF-only deck with no interactive app slides — just shows the
generated example figures compiled into Beamer.
"""

# No interactive app slides in this presentation
APP_SLIDES: dict = {}


def build_slides(pdf_page_count: int) -> list[tuple[str, int | str]]:
    """Return all PDF pages in order."""
    return [("pdf", i) for i in range(pdf_page_count)]
