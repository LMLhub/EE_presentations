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
│   └── preamble.tex           # Shared Beamer macros & theme
├── presentations/
│   └── 20260326-01-01/        # One folder per presentation
│       ├── main.tex           # LaTeX / Beamer source
│       ├── main.pdf           # Compiled PDF
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

---

### 4 — Add interactive Streamlit slides

Slides are a mix of PDF pages and live Streamlit apps. To add a new interactive slide:

**Step 1** — write a function in `presentation.py`:

```python
def my_slide() -> None:
    st.subheader("My interactive slide")
    x = st.slider("x", 0.0, 10.0, 5.0)
    st.write(f"x² = {x**2:.2f}")
```

**Step 2** — register it in `APP_SLIDES`:

```python
APP_SLIDES: dict = {
    "demo": app_slide_demo,
    "mine": my_slide,       # ← add this
}
```

**Step 3** — place it in the deck by editing `build_slides()`:

```python
slides.append(("pdf", 3))        # PDF page 4 (0-based)
slides.append(("app", "mine"))   # your interactive slide
slides.append(("pdf", 4))        # PDF page 5
```

Each entry is either `("pdf", page_index)` (0-based) or `("app", key)`.

---

## File overview

| File | Purpose |
|---|---|
| `presentations/*/main.tex` | LaTeX / Beamer source for each talk |
| `shared/preamble.tex` | Shared macros & Beamer theme |
| `build.sh` | Compile a presentation: `./build.sh presentations/<name>` |
| `presentation.py` | Streamlit viewer: `streamlit run presentation.py -- presentations/<name>` |
| `environment.yml` | Conda environment definition |
