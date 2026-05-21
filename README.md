# Distribution Calculator

A Python desktop application for visualising and computing probabilities for statistical distributions, built with tkinter and matplotlib.

> **Branch note:** `feature/window-menu` adds a top menu bar and a per-distribution info viewer. **Info → About** now opens a Toplevel window showing a reference PDF for the currently selected distribution (rendered via PyMuPDF). Only `normal.pdf`, `binomial.pdf`, and `levey.pdf` have real content so far — the other distributions point at `normal.pdf` as a placeholder.

## Features

- Interactive GUI with an embedded matplotlib canvas
- Top menu bar: **File**, **Window**, **Help**, **Info**
- Select distributions from a scrollable list on the left
- Configurable parameters via input spinboxes
- Probability calculations displayed in a result box
- Per-distribution reference PDFs rendered in a popup window

## Menu Bar

- **File → Save** — saves the current figure as an image. Opens a Save As dialog pre-filled with `{distribution}_{timestamp}.png`; matplotlib infers the format from the chosen extension (PNG, PDF, or SVG)
- **Window → New Window** — launches a second instance of the calculator in a separate process
- **Help → About** — placeholder
- **Info → About** — opens a Toplevel window displaying the reference PDF for the currently selected distribution, rendered by `PDF_reader.show_pdf` (PyMuPDF + a tkinter Canvas with vertical scroll and mouse-wheel support)

## Distributions

Most univariate distributions share the same four-mode dropdown:

- **Curve** — plot the PDF (or PMF for discrete distributions)
- **P(X ≤ x)** — left-tail probability with shaded area
- **P(X ≥ x)** — right-tail probability with shaded area
- **P(a ≤ X ≤ b)** — interval probability with shaded area

### Normal
Configurable mean (μ) and standard deviation (σ).

### Binomial
Bar chart of the PMF with the selected region highlighted. The exact mode is **P(X = k)** instead of `Curve`, highlighting the *k*-th bar.

### Lévy
Configurable location (μ) and scale (c).

### Slash
The standard slash distribution (ratio of a standard normal and an independent uniform). No shape parameters.

### Benini
Configurable α, β, and σ, with a toggle between natural-log (base *e*) and base-10 formulations.

### Reciprocal
Configurable support endpoints *a* and *b*.

### Raised Cosine
Configurable mean (μ) and scale (s).

### Kumaraswamy
Configurable shape parameters *a* and *b* on the support [0, 1].

### Cauchy
Configurable location (x₀) and scale (γ). Heavy-tailed and symmetric about x₀; plotted over x₀ ± 10γ to show the slow tail decay.

### Bivariate Normal
3D surface plot of the joint PDF. Configurable means, variances, and correlation.

## Requirements

```
numpy
matplotlib
scipy
PyMuPDF              # imported as `fitz`, used by PDF_reader.py
tkinter (included with standard Python)
```

Install dependencies:

```bash
pip install numpy matplotlib scipy PyMuPDF
```

## Usage

Run the application from the project root:

```bash
python Calculator_GUI.py
```

## Project Structure

```
Distribution Calculator/
├── Calculator_GUI.py              # Window setup, menu bar, listbox, canvas, distribution registry
├── PDF_reader.py                  # show_pdf(master, pdf_path, width, height) — renders a PDF in a scrollable tk Canvas
├── pdfs/                          # Reference PDFs shown by Info → About
│   ├── normal.pdf
│   ├── binomial.pdf
│   └── levey.pdf
├── Distributions/                 # Pure maths — no tkinter imports
│   ├── __init__.py
│   ├── Normal_dist.py
│   ├── Binomial_dist.py
│   ├── Levy_dist.py
│   ├── Slash_dist.py
│   ├── Benini_dist.py
│   ├── Reciprocal_dist.py
│   ├── Raised_cosine_dist.py
│   ├── Kumaraswamy_dist.py
│   ├── Cauchy_dist.py
│   └── Multivariate_normal.py
└── Panels/                        # GUI panels — one file per distribution
    ├── __init__.py
    ├── normal_panel.py
    ├── Binomial_panel.py
    ├── Levy_panel.py
    ├── Slash_panel.py
    ├── Benini_panel.py
    ├── Reciprocal_panel.py
    ├── Raised_cosine_panel.py
    ├── Kumaraswamy_panel.py
    ├── Cauchy_panel.py
    └── bivariate_panel.py
```

## Planned Features

More distributions:
1. ~~Benini distribution~~
2. ~~Reciprocal distribution~~
3. ~~Raised cosine~~
4. ~~Kumaraswamy distribution~~
5. Bivariate Cauchy
6. Dirichlet (k=3)
7. Bivariate Laplace
8. Copula surfaces
9. Hyper-Erlang
10. Muth distribution
11. Gompertz distribution

GUI updates:
- Themes
- Info section for distributions
- Reference PDFs for the remaining distributions (currently only Normal, Binomial, and Lévy have real content — the others fall back to `normal.pdf`)
- Look-up table generator

## Adding a New Distribution

1. Add the maths to a new file in `Distributions/` — functions must accept `ax` as their first parameter and must not call `plt.show()`
2. Create a panel file in `Panels/` with a `draw_*` function that accepts `(input_frame, fig, canvas)` and handles all widget creation and plotting
3. Drop a reference PDF into `pdfs/` (or reuse an existing one as a placeholder)
4. Import the panel function in `Calculator_GUI.py` and add one entry to the `DISTRIBUTIONS` dict in the form `"Name": [draw_fn, "pdfs/your_file.pdf"]` — the panel callable and PDF path are looked up by the listbox selection and the Info menu respectively
