# Distribution Calculator

A Python desktop application for visualising and computing probabilities for statistical distributions, built with tkinter and matplotlib.

Every distribution is described as a single declarative **spec** in `New_Distributions.py`; one shared engine turns each spec into both its maths and its input panel. Adding a new distribution is "write one spec, add one line to the registry" — no new files and no GUI boilerplate.

## Features

- Interactive GUI with an embedded matplotlib canvas
- Top menu bar: **File**, **Window**, **Info**
- Select distributions from a scrollable list on the left
- Configurable parameters via input spinboxes
- Probability calculations displayed in a result box
- Per-distribution reference PDFs rendered in a popup window

## Architecture

All distribution logic lives in [`New_Distributions.py`](New_Distributions.py):

- **`Param`** — describes one input spinbox (label, the keyword its value is passed under, default, range, step).
- **`Distribution`** — base class holding the shared scaffolding (parameter spinboxes, the result box, the Plot button) and the single `draw(input_frame, fig, canvas)` entry point the GUI calls.
- **Three families** subclass it, each containing the *only* copy of the logic that used to be duplicated per distribution:
  - **`ContinuousDistribution`** — the four-mode dropdown (Curve / P(X ≤ x) / P(X ≥ x) / P(a ≤ X ≤ b)) with numerically integrated, shaded probabilities. Optional `variants` support alternate formulas (used by Benini's ln vs log₁₀ toggle).
  - **`DiscreteDistribution`** — a PMF bar chart with the selected region highlighted via bar alpha.
  - **`SurfaceDistribution`** — a 3D `plot_surface` with a **View** selector (3D / XZ / YZ / XY).
- **`DISTRIBUTIONS`** — the registry dict (`"Name": spec`) that [`Calculator_GUI.py`](Calculator_GUI.py) reads to populate the listbox and the Info menu. Each spec also carries an `info_pdf` path.

`Calculator_GUI.py` imports `DISTRIBUTIONS` and calls `DISTRIBUTIONS[name].draw(...)` — one call produces any distribution's panel and plot.

## Menu Bar

- **File → Save** — saves the current figure as an image. Opens a Save As dialog pre-filled with `{distribution}_{timestamp}.png`; matplotlib infers the format from the chosen extension (PNG, PDF, or SVG)
- **Window → New Window** — launches a second instance of the calculator in a separate process
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

### Student's t
Configurable degrees of freedom (ν). Symmetric, heavy-tailed; approaches the standard normal as ν grows.

### Chi-squared
Configurable degrees of freedom (k). Supported on x ≥ 0, with the plot range scaled to k + 4√(2k) to capture the bulk of the mass.

The three bivariate/multivariate distributions render as 3D surface plots and share a **View** selector (3D, XZ, YZ, XY) that re-orients the camera to the requested orthographic plane.

### Bivariate Normal
3D surface plot of the joint PDF. Configurable means, standard deviations, and correlation (ρ).

### Bivariate Cauchy
3D surface plot of the joint PDF. Configurable scales, locations, and correlation (ρ). The standard bivariate Cauchy is the special case scale = 1, location = 0, ρ = 0.

### Dirichlet
3D surface plot over the unit square. Configurable shape parameters α and β.

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
├── New_Distributions.py           # The engine: Param, Distribution base + 3 family
│                                   # subclasses, all distribution specs, and the
│                                   # DISTRIBUTIONS registry
├── Calculator_GUI.py              # Window setup, menu bar, listbox, canvas; reads DISTRIBUTIONS
├── PDF_reader.py                  # show_pdf(master, pdf_path, width, height) — renders a PDF in a scrollable tk Canvas
├── pdfs/                          # Reference PDFs shown by Info → About
│   ├── normal.pdf
│   ├── binomial.pdf
│   └── levey.pdf
├── Distributions/                 # (legacy package, now empty)
│   └── __init__.py
└── Panels/                        # (legacy package, now empty)
    └── __init__.py
```

## Adding a New Distribution

Everything happens in [`New_Distributions.py`](New_Distributions.py):

1. **Write one spec** — an instance of the family that fits:
   - `ContinuousDistribution(...)` — supply the `pdf` formula, a list of `Param`s, a `plot_range`, and the integration `support`. (Use `variants` for alternate formulas.)
   - `DiscreteDistribution(...)` — supply the `pmf`, `Param`s, the `k_param`, and the integer `support`.
   - `SurfaceDistribution(...)` — supply a `surface(ax, **params)` function and its `Param`s.
   Optionally set `info_pdf` to a file in `pdfs/` for the Info menu (defaults to `pdfs/normal.pdf`).
2. **Register it** — add one line to the `DISTRIBUTIONS` dict: `"Name": your_spec`.

No new files, no tkinter code, and no changes to `Calculator_GUI.py`.

## Planned Features

More distributions:
1. ~~Benini distribution~~
2. ~~Reciprocal distribution~~
3. ~~Raised cosine~~
4. ~~Kumaraswamy distribution~~
5. ~~Bivariate Cauchy~~
6. ~~Dirichlet~~
7. ~~Student's t~~
8. ~~Chi-squared~~
9. Bivariate Laplace
10. Copula surfaces
11. Hyper-Erlang
12. Muth distribution
13. Gompertz distribution

GUI updates:
- Themes
- Reference PDFs for the remaining distributions (currently only Normal, Binomial, and Lévy have real content — the others fall back to `normal.pdf`)
- Look-up table generator
