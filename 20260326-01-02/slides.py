"""
Slide map for the presentation.

Each entry is one of:
  ("pdf", page_number)   — renders that page from presentation.pdf
  ("app", key)           — runs the corresponding interactive Streamlit app

PDF page numbers are 1-indexed and match the compiled presentation.pdf.

Slide structure
───────────────
 1  pdf 1   Title
 2  pdf 2   Misconception: EE ≠ log transform
 3  app     additive_window    — additive dynamic, sliding window shows constant δx
 4  app     multiplicative_window — multiplicative dynamic, δx grows with wealth
 4b app     clock_speed        — 3 anchors show clock rotation shrinks at higher x
 4t app     log_transform      — apply ln: δ(ln x) is constant (correct clock)
 5  pdf 3   Power-law derivation: x→xᵅ ⟹ φ = ln ln x
 5b app     power_law_worlds   — power-law shown in x and ln(x) worlds (both fail)
 5t app     loglog_window      — ln(ln(x)) gives constant increments
 6  app     three_clocks       — 3×3 summary grid: dynamics × clock domains
 7  pdf 4   Absorbing boundaries
 8  pdf 5   Summary
"""

from interactive.additive_window_slide       import additive_window_slide
from interactive.multiplicative_window_slide import multiplicative_window_slide
from interactive.clock_speed_slide          import clock_speed_slide
from interactive.log_transform_slide        import log_transform_slide
from interactive.power_law_worlds_slide     import power_law_worlds_slide
from interactive.loglog_window_slide        import loglog_window_slide
from interactive.three_clocks_slide         import three_clocks_slide

APP_SLIDES = {
    "additive_window":       additive_window_slide,
    "multiplicative_window": multiplicative_window_slide,
    "clock_speed":           clock_speed_slide,
    "log_transform":         log_transform_slide,
    "power_law_worlds":      power_law_worlds_slide,
    "loglog_window":         loglog_window_slide,
    "three_clocks":          three_clocks_slide,
}

SLIDES = [
    ("pdf", 1),                       # 1  — Title
    ("pdf", 2),                       # 2  — Misconception
    ("app", "additive_window"),       # 3  — Additive window
    ("app", "multiplicative_window"), # 4  — Multiplicative window
    ("app", "clock_speed"),           # 4b — Clock speed solution
    ("app", "log_transform"),         # 4t — Log-transform solution
    ("pdf", 3),                       # 5  — Power-law derivation
    ("app", "power_law_worlds"),      # 5b — Power-law in x and ln(x)
    ("app", "loglog_window"),         # 5t — Power-law in ln(ln(x))
    ("app", "three_clocks"),          # 6  — Three clocks summary
    ("pdf", 4),                       # 7  — Absorbing boundaries
    ("pdf", 5),                       # 8  — Summary
]
