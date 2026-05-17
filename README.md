# Distribution Calculator

A Python desktop application for visualising and computing probabilities for statistical distributions, built with tkinter and matplotlib.

## Features

- Interactive GUI with an embedded matplotlib canvas
- Select distributions from a scrollable list
- Configurable parameters via input spinboxes
- Probability calculations displayed in the app

## Distributions

### Normal Distribution
- Plot the probability density curve for any mean and standard deviation
- Four modes selectable from a dropdown:
  - **Curve** — plot the PDF
  - **P(X < x)** — left-tail probability with shaded area
  - **P(X > x)** — right-tail probability with shaded area
  - **P(a < X < b)** — interval probability with shaded area
- Computed probabilities displayed in a result text box

### Bivariate Normal Distribution
- 3D surface plot of the joint PDF
- Configurable means, variances, and correlation

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
├── Calculator_GUI.py          # Main GUI application
└── Distributions/
    ├── __init__.py
    ├── Normal_dist.py         # Normal distribution functions (N, N_left, N_right, N_dual)
    └── Multivariate_normal.py # Bivariate normal distribution (binorm)
```

## Adding a New Distribution

1. Create a new file in `Distributions/` with a draw function that accepts a matplotlib `ax` as its first argument
2. Import it in `Calculator_GUI.py`
3. Add a `draw_*` function and register it in the `DISTRIBUTIONS` dictionary
