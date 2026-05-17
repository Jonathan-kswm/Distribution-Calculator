# Distribution Calculator

A Python desktop application for visualising and computing probabilities for statistical distributions, built with tkinter and matplotlib.

## Features

- Interactive GUI with an embedded matplotlib canvas
- Select distributions from a scrollable list on the left
- Configurable parameters via input spinboxes
- Probability calculations displayed in a result box

## Distributions

### Normal Distribution
- Plot the probability density curve for any mean and standard deviation
- Four modes selectable from a dropdown:
  - **Curve** — plot the PDF
  - **P(X ≤ x)** — left-tail probability with shaded area
  - **P(X ≥ x)** — right-tail probability with shaded area
  - **P(a ≤ X ≤ b)** — interval probability with shaded area

### Bivariate Normal Distribution
- 3D surface plot of the joint PDF
- Configurable means, variances, and correlation

### Binomial Distribution
- Bar chart of the PMF with the selected region highlighted
- Four modes:
  - **P(X = k)** — exact probability, highlighting the kth bar
  - **P(X ≤ k)** — left cumulative probability
  - **P(X ≥ k)** — right cumulative probability
  - **P(a ≤ X ≤ b)** — interval probability

## Requirements

```
numpy
matplotlib
scipy
tkinter (included with standard Python)
```

Install dependencies:

```bash
pip install numpy matplotlib scipy
```

## Usage

Run the application from the project root:

```bash
python Calculator_GUI.py
```

## Project Structure

```
Distribution Calculator/
├── Calculator_GUI.py              # Window setup, listbox, canvas, distribution registry
├── Distributions/                 # Pure maths — no tkinter imports
│   ├── __init__.py
│   ├── Normal_dist.py             # N, N_left, N_right, N_dual
│   ├── Multivariate_normal.py     # binorm
│   └── Binomial_dist.py           # Bin_equal, Bin_left, Bin_right, Bin_between
└── Panels/                        # GUI panels — one file per distribution
    ├── __init__.py
    ├── normal_panel.py            # draw_normal(input_frame, fig, canvas)
    ├── bivariate_panel.py         # draw_bivariate(input_frame, fig, canvas)
    └── Binomial_panel.py          # draw_binomial(input_frame, fig, canvas)
```
## Planned Features
More Distrributions:
1. Benini distribution
2. Reciprocal distribution
3. Raised cosine
4. Kumaraswamy distribution
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
- look up table generator

## Adding a New Distribution

1. Add the maths to a new file in `Distributions/` — functions must accept `ax` as their first parameter and must not call `plt.show()`
2. Create a panel file in `Panels/` with a `draw_*` function that accepts `(input_frame, fig, canvas)` and handles all widget creation and plotting
3. Import the panel function in `Calculator_GUI.py` and add one entry to the `DISTRIBUTIONS` dict
