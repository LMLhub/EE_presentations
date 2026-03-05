Templates for presentations based on Peters and Adamou, *An Introduction to Ergodicity Economics,* LML Press, 2025.

<p align="center">
  <img src="shared/An_Introduction_to_Ergodicity_Economics_front.png" width="50%">
</p>

---

## Project structure

```
EE_presentations/
├── README.md
├── environment.yml            # Conda / pip dependencies
├── presentation.py            # Streamlit presentation viewer
├── build.sh                   # Compile LaTeX → PDF
├── shared/
│   ├── preamble.tex           # Shared Beamer macros, theme & logos
│   ├── logos/                 # LML logo images (sidebar + full)
│   ├── plotting/              # Shared matplotlib styling & utilities
│   │   ├── __init__.py
│   │   └── base.py
│   └── figure-config.yaml     # Default figure-generation config template
├── presentations/
│   ├── example-figs/          # Demo: generating & displaying figures
│   │   ├── generate-figs.py   # Script to create figures using shared/plotting
│   │   ├── figure-config.yaml # Local config (output to ./figs/)
│   │   ├── main.tex / slides.py / figs/
│   └── 20260326-01-01/        # One folder per presentation
│       ├── main.tex           # LaTeX / Beamer source
│       ├── main.pdf           # Compiled PDF
│       ├── slides.py          # Slide deck definition (app slides + ordering)
│       └── figs/              # Figures used in this presentation
```

---

## Setup

Create and activate the conda environment (one-time):

```bash
conda env create -f environment.yml
conda activate ee_presentations
```

---

## Workflow

### 1 — Write slides in LaTeX

Each presentation lives in its own folder under `presentations/`. Edit
`main.tex` inside that folder, then compile to PDF:

```bash
./build.sh presentations/20260326-01-01
```

This runs `pdflatex` twice (required for Beamer cross-references) and removes all auxiliary files, leaving only `main.pdf`.

---

### 2 — Run the browser presentation

```bash
conda activate ee_presentations
streamlit run presentation.py -- presentations/20260326-01-01
```

The presentation opens automatically at `http://localhost:8501`.

**Navigation:** use the **← →** (or **↑ ↓**) arrow keys to move between slides.
The slide fills the full browser window; zoom the browser to taste.

---

### 3 — Create a new presentation

```bash
mkdir -p presentations/YYYYMMDD-NN-NN/figs
```

Create a `main.tex` that starts with:

```latex
\input{../../shared/preamble.tex}

\title{...}
\author{...}
\date{...}

\begin{document}
  ...
\end{document}
```

The shared preamble provides all macros and the Beamer theme.

Optionally create a `slides.py` in the same folder to add interactive
Streamlit slides (see next section). If omitted, the deck is pure PDF.

---

### 4 — Add interactive Streamlit slides

Slides are a mix of PDF pages and live Streamlit apps. To add an
interactive slide, create a `slides.py` in your presentation folder:

**Step 1** — write a function:

```python
def my_slide() -> None:
    st.subheader("My interactive slide")
    x = st.slider("x", 0.0, 10.0, 5.0)
    st.write(f"x² = {x**2:.2f}")
```

**Step 2** — register it in `APP_SLIDES`:

```python
APP_SLIDES: dict = {
    "mine": my_slide,
}
```

**Step 3** — define the deck order in `SLIDES`:

```python
SLIDES: list = [
    ("pdf", 0),         # PDF page 1 (0-based)
    ("pdf", 1),         # PDF page 2
    ("pdf", 2),         # PDF page 3
    ("app", "mine"),    # your interactive slide
    ("pdf", 3),         # PDF page 4
]
```

Each entry is either `("pdf", page_index)` (0-based) or `("app", key)`.
If `SLIDES` is not defined, all PDF pages are shown in order.

---

### 5 — Generate figures with consistent styling

A shared plotting module (`shared/plotting/`) provides consistent matplotlib
styling across all presentations. Each presentation can include a
`generate-figs.py` script to create its figures:

```bash
cd presentations/example-figs
python generate-figs.py figure-config.yaml
```

The script imports from `shared.plotting` and saves PDFs into the local
`figs/` folder, ready to be included by `main.tex`.

See `presentations/example-figs/` for a complete working example.

**Creating a figure script for a new presentation:**

1. Copy `presentations/example-figs/generate-figs.py` and
   `presentations/example-figs/figure-config.yaml` into your presentation folder
2. Edit `generate-figs.py` to generate your figures
3. Run it, then compile the LaTeX: `./build.sh presentations/<name>`

---

## File overview

| File | Purpose |
|---|---|
| `presentations/*/main.tex` | LaTeX / Beamer source for each talk |
| `presentations/*/slides.py` | Slide deck definition (app slides + ordering) |
| `shared/preamble.tex` | Shared macros, Beamer theme & logo definitions |
| `shared/logos/` | LML logo images (auto-included via preamble) |
| `shared/plotting/` | Shared matplotlib styling & utilities |
| `shared/figure-config.yaml` | Default figure-generation config template |
| `build.sh` | Compile a presentation: `./build.sh presentations/<name>` |
| `presentation.py` | Streamlit viewer: `streamlit run presentation.py -- presentations/<name>` |
| `environment.yml` | Conda environment definition |
