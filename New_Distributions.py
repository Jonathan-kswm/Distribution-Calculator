# -*- coding: utf-8 -*-
"""
Spec-driven distribution engine.

Every probability distribution in the calculator is described here as a single
declarative object (formula + parameters + ranges).  A shared engine turns any
such spec into both its maths and its Tkinter input panel, so adding a new
distribution is "write one spec, add one line to DISTRIBUTIONS" -- no new files
and no Tkinter boilerplate.

Three families are supported:
  * ContinuousDistribution -- curve / P(X<=x) / P(X>=x) / P(a<=X<=b) with a
    shaded integral (Normal, Cauchy, Levy, Slash, Benini, Reciprocal,
    Raised cosine, Kumaraswamy, Student's t, Chi-squared).
  * DiscreteDistribution -- bar chart with alpha shading (Binomial).
  * SurfaceDistribution -- 3D plot_surface with a 3D/XZ/YZ/XY view selector
    (Bivariate Normal, Bivariate Cauchy, Dirichlet).
"""

import tkinter as tk
from tkinter import ttk

import math
import numpy as np
import scipy.integrate as integrate
from scipy.special import gamma

from matplotlib import cm
from matplotlib.ticker import LinearLocator


# --------------------------------------------------------------------------- #
# Parameter helper                                                            #
# --------------------------------------------------------------------------- #
class Param:
    """One labelled input spinbox.  ``symbol`` is the keyword the value is
    passed under to the distribution's formula / range callables."""

    def __init__(self, label, symbol, default, lo=-1000, hi=1000, increment=1):
        self.label = label
        self.symbol = symbol
        self.default = default
        self.lo = lo
        self.hi = hi
        self.increment = increment


# --------------------------------------------------------------------------- #
# Base class                                                                  #
# --------------------------------------------------------------------------- #
class Distribution:
    """Shared scaffolding.  ``draw`` is the single entry point the GUI calls to
    build a distribution's whole input panel + plot."""

    OPS = ["Curve", "P(X≤x)", "P(X≥x)", "P(a≤X≤b)"]

    def __init__(self, name, params, info_pdf="pdfs/normal.pdf"):
        self.name = name
        self.params = params
        self.info_pdf = info_pdf

    def _add_param_spinboxes(self, frame):
        """Create a labelled spinbox per Param; return a getter that reads them
        into a ``{symbol: float}`` dict."""
        spins = {}
        for p in self.params:
            tk.Label(frame, text=p.label).pack()
            sb = tk.Spinbox(frame, from_=p.lo, to=p.hi, increment=p.increment,
                            textvariable=tk.StringVar(value=str(p.default)))
            sb.pack()
            spins[p.symbol] = sb
        return lambda: {sym: float(sb.get()) for sym, sb in spins.items()}

    @staticmethod
    def _add_extra_spin(frame, label, value):
        tk.Label(frame, text=label).pack()
        sb = tk.Spinbox(frame, from_=-1000, to=1000, increment=0.1,
                        textvariable=tk.StringVar(value=str(value)))
        sb.pack()
        return sb

    def draw(self, input_frame, fig, canvas):
        raise NotImplementedError


# --------------------------------------------------------------------------- #
# Univariate continuous                                                       #
# --------------------------------------------------------------------------- #
class ContinuousDistribution(Distribution):
    def __init__(self, name, params, pdf, plot_range, support,
                 x_default=0.0, lo_default=-0.25, hi_default=0.25,
                 n_points=500, axhline=False, variants=None,
                 variant_label="Variant", le_note="", text_height=2,
                 info_pdf="pdfs/normal.pdf"):
        super().__init__(name, params, info_pdf)
        self.pdf = pdf
        self.plot_range = plot_range
        self.support = support
        self.x_default = x_default
        self.lo_default = lo_default
        self.hi_default = hi_default
        self.n_points = n_points
        self.axhline = axhline
        # variants: optional list of (label, pdf) for distributions that offer
        # alternate formulas (e.g. Benini's ln vs log10).  When set, the panel
        # shows a selector and ignores self.pdf.
        self.variants = variants
        self.variant_label = variant_label
        self.le_note = le_note          # appended to the P(X<=x) result text
        self.text_height = text_height

    def draw(self, input_frame, fig, canvas):
        variant_choice = None
        if self.variants:
            variant_choice = tk.StringVar(value=self.variants[0][0])
            tk.Label(input_frame, text=self.variant_label).pack()
            for label, _fn in self.variants:
                tk.Radiobutton(input_frame, text=label, variable=variant_choice,
                               value=label, command=lambda: plot()).pack()

        get_params = self._add_param_spinboxes(input_frame)

        combo = ttk.Combobox(input_frame, values=self.OPS, state="readonly")
        combo.pack(pady=10)
        combo.set("Curve")

        extra = tk.Frame(input_frame)
        extra.pack()

        text = tk.Text(input_frame, height=self.text_height, width=20)

        def current_pdf():
            if self.variants:
                for label, fn in self.variants:
                    if label == variant_choice.get():
                        return fn
            return self.pdf

        def update_extra(event=None):
            for w in extra.winfo_children():
                w.destroy()
            sel = combo.get()
            if sel in ("P(X≤x)", "P(X≥x)"):
                self._add_extra_spin(extra, "x", self.x_default)
            elif sel == "P(a≤X≤b)":
                self._add_extra_spin(extra, "a (lower)", self.lo_default)
                self._add_extra_spin(extra, "b (upper)", self.hi_default)
            plot()

        combo.bind("<<ComboboxSelected>>", update_extra)
        text.pack(pady=15)

        def plot():
            params = get_params()
            f = lambda x: current_pdf()(x, **params)
            lo, hi = self.plot_range(**params)
            sup_lo, sup_hi = self.support(**params)

            fig.clear()
            ax = fig.add_subplot(111)
            x = np.linspace(lo, hi, self.n_points)
            sel = combo.get()
            spins = [w for w in extra.winfo_children() if isinstance(w, tk.Spinbox)]
            text.delete("1.0", tk.END)

            if sel == "P(X≤x)":
                xv = float(spins[0].get())
                prob, _ = integrate.quad(f, sup_lo, xv)
                xf = np.linspace(lo, xv, self.n_points)
                ax.fill_between(xf, f(xf), alpha=0.4)
                text.insert(tk.END, f"P(X ≤ {xv}) = {prob:.4f}{self.le_note}")
            elif sel == "P(X≥x)":
                xv = float(spins[0].get())
                prob, _ = integrate.quad(f, xv, sup_hi)
                xf = np.linspace(xv, hi, self.n_points)
                ax.fill_between(xf, f(xf), alpha=0.4)
                text.insert(tk.END, f"P(X ≥ {xv}) = {prob:.4f}")
            elif sel == "P(a≤X≤b)":
                a = float(spins[0].get())
                b = float(spins[1].get())
                prob, _ = integrate.quad(f, a, b)
                xf = np.linspace(a, b, self.n_points)
                ax.fill_between(xf, f(xf), alpha=0.4)
                text.insert(tk.END, f"P({a} ≤ X ≤ {b}) = {prob:.4f}")

            ax.plot(x, f(x))
            if self.axhline:
                ax.axhline(0, color="black", linewidth=0.5)
            canvas.draw()

        tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
        plot()


# --------------------------------------------------------------------------- #
# Discrete                                                                    #
# --------------------------------------------------------------------------- #
class DiscreteDistribution(Distribution):
    OPS = ["P(X =k)", "P(X≤x)", "P(X≥x)", "P(b≤X≤a)"]

    def __init__(self, name, params, k_param, pmf, support,
                 a_default=4, b_default=2, info_pdf="pdfs/normal.pdf"):
        super().__init__(name, params, info_pdf)
        self.k_param = k_param
        self.pmf = pmf
        self.support = support      # (**params) -> integer x array
        self.a_default = a_default  # upper of the between-region
        self.b_default = b_default  # lower of the between-region

    def draw(self, input_frame, fig, canvas):
        get_params = self._add_param_spinboxes(input_frame)

        kp = self.k_param
        tk.Label(input_frame, text=kp.label).pack()
        k_sb = tk.Spinbox(input_frame, from_=kp.lo, to=kp.hi,
                          textvariable=tk.StringVar(value=str(kp.default)))
        k_sb.pack()

        combo = ttk.Combobox(input_frame, values=self.OPS, state="readonly")
        combo.pack(pady=10)
        combo.set("P(X =k)")

        extra = tk.Frame(input_frame)
        extra.pack()

        text = tk.Text(input_frame, height=2, width=20)

        def update_extra(event=None):
            for w in extra.winfo_children():
                w.destroy()
            if combo.get() == "P(b≤X≤a)":
                self._add_extra_spin(extra, "a (upper)", self.a_default)
                self._add_extra_spin(extra, "b (lower)", self.b_default)
            plot()

        combo.bind("<<ComboboxSelected>>", update_extra)
        text.pack(pady=15)

        def plot():
            params = get_params()
            k = int(float(k_sb.get()))
            fig.clear()
            ax = fig.add_subplot(111)
            x = self.support(**params)
            y = [self.pmf(int(i), **params) for i in x]
            bars = ax.bar(x, y)
            sel = combo.get()
            spins = [w for w in extra.winfo_children() if isinstance(w, tk.Spinbox)]
            text.delete("1.0", tk.END)

            if sel == "P(X =k)":
                for idx, bar in enumerate(bars):
                    if idx != k:
                        bar.set_alpha(0.3)
                text.insert(tk.END, f"P(X = {k}) = {self.pmf(k, **params):.4f}")
            elif sel == "P(X≤x)":
                for idx, bar in enumerate(bars):
                    if idx > k:
                        bar.set_alpha(0.3)
                text.insert(tk.END, f"P(X ≤ {k}) = {sum(y[:k + 1]):.4f}")
            elif sel == "P(X≥x)":
                for idx, bar in enumerate(bars):
                    if idx < k:
                        bar.set_alpha(0.3)
                text.insert(tk.END, f"P(X ≥ {k}) = {sum(y[k:]):.4f}")
            elif sel == "P(b≤X≤a)":
                upper = int(float(spins[0].get()))
                lower = int(float(spins[1].get()))
                for idx, bar in enumerate(bars):
                    if idx < lower or idx > upper:
                        bar.set_alpha(0.3)
                prob = sum(y[lower:upper + 1])
                text.insert(tk.END, f"P({upper} ≥ X ≥ {lower}) = {prob:.4f}")
            canvas.draw()

        tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
        plot()


# --------------------------------------------------------------------------- #
# 3D surface                                                                  #
# --------------------------------------------------------------------------- #
class SurfaceDistribution(Distribution):
    # view name -> (elev, azim); None means the default interactive 3D view.
    VIEWS = {"3D": None, "XZ": (0, -90), "YZ": (0, 0), "XY": (90, -90)}

    def __init__(self, name, params, surface, info_pdf="pdfs/normal.pdf"):
        super().__init__(name, params, info_pdf)
        self.surface = surface      # surface(ax, **params)

    def draw(self, input_frame, fig, canvas):
        get_params = self._add_param_spinboxes(input_frame)

        # reserved for future readouts, kept for layout parity with old panels
        tk.Text(input_frame, height=6, width=20).pack(pady=15)

        view = tk.StringVar(value="3D")

        def plot():
            params = get_params()
            fig.clear()
            ax = fig.add_subplot(111, projection="3d")
            angles = self.VIEWS[view.get()]
            if angles is not None:
                ax.set_proj_type("ortho")
                ax.view_init(elev=angles[0], azim=angles[1], roll=0)
            self.surface(ax, **params)
            canvas.draw()

        tk.Label(input_frame, text="View:").pack()
        for vname in ("3D", "XZ", "YZ", "XY"):
            tk.Radiobutton(input_frame, text=vname, variable=view,
                           value=vname, command=plot).pack()

        tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
        plot()


# --------------------------------------------------------------------------- #
# Formulae for the special cases                                              #
# --------------------------------------------------------------------------- #
_PHI0 = 1 / np.sqrt(2 * np.pi)


def _slash_pdf(x):
    x = np.asarray(x, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        y = _PHI0 * (1 - np.exp(-0.5 * x ** 2)) / x ** 2
    return np.where(x == 0, _PHI0 / 2, y)


def _benini_e(x, a, b, s):
    L = np.log(x / s)
    return np.exp(-a * L - b * L ** 2) * (a / x + (2 * b * L) / x)


def _benini_10(x, a, b, s):
    L = np.log10(x / s)
    return np.exp(-a * L - b * L ** 2) * (a / x + (2 * b * L) / x)


def _chi2_pdf(x, k):
    return (1.0 / (2 ** (k / 2) * gamma(k / 2))) * x ** (k / 2 - 1) * np.exp(-x / 2)


def _t_pdf(x, df):
    return (gamma((df + 1) / 2) / (np.sqrt(df * np.pi) * gamma(df / 2))
            * (1 + x ** 2 / df) ** (-(df + 1) / 2))


def _style_surface(ax, X, Y, Z):
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Prob")
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    ax.set_zlim(0, 1.5 * Z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter("{x:.02f}")


def _binorm_surface(ax, mean_x, mean_y, sd_x, sd_y, corr):
    X = np.arange(mean_x - 3 * sd_x, mean_x + 3 * sd_x, 0.25)
    Y = np.arange(mean_y - 3 * sd_y, mean_y + 3 * sd_y, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = (((X - mean_x) / sd_x) ** 2
         - 2 * corr * ((X - mean_x) / sd_x) * ((Y - mean_y) / sd_y)
         + ((Y - mean_y) / sd_y) ** 2)
    Z = (1 / (2 * np.pi * sd_x * sd_y * np.sqrt(1 - corr ** 2))) \
        * np.exp((-1 / (2 * (1 - corr ** 2))) * R)
    _style_surface(ax, X, Y, Z)


def _bivariate_cauchy_surface(ax, scale_x, scale_y, loc_x, loc_y, corr):
    X = np.arange(loc_x - 4 * scale_x, loc_x + 4 * scale_x, 0.1)
    Y = np.arange(loc_y - 4 * scale_y, loc_y + 4 * scale_y, 0.1)
    X, Y = np.meshgrid(X, Y)
    Z = (1 / (2 * np.pi * scale_x * scale_y * np.sqrt(1 - corr ** 2))) * (
        1 + (1 / (1 - corr ** 2)) * (
            ((X - loc_x) ** 2 / scale_x ** 2)
            - (2 * corr * (X - loc_x) * (Y - loc_y)) / (scale_x * scale_y)
            + ((Y - loc_y) ** 2) / scale_y ** 2)) ** (-3 / 2)
    _style_surface(ax, X, Y, Z)


def _dirichlet_surface(ax, a, b):
    X = np.arange(0, 1, 0.01)
    Y = np.arange(0, 1, 0.01)
    X, Y = np.meshgrid(X, Y)
    B = (gamma(a) * gamma(b)) / gamma(a + b)
    Z = (B ** -1) * (X ** (a - 1) * Y ** (b - 1))
    _style_surface(ax, X, Y, Z)


# --------------------------------------------------------------------------- #
# Specs                                                                       #
# --------------------------------------------------------------------------- #
normal = ContinuousDistribution(
    "Normal",
    params=[Param("Mean", "mean", 0), Param("SD", "sd", 1, lo=0)],
    pdf=lambda x, mean, sd: (1 / (np.sqrt(2 * np.pi) * sd))
        * np.exp(-0.5 * ((x - mean) / sd) ** 2),
    plot_range=lambda mean, sd: (mean - 4 * sd, mean + 4 * sd),
    support=lambda mean, sd: (-np.inf, np.inf),
    x_default=0, lo_default=-0.25, hi_default=0.25, n_points=500,
    info_pdf="pdfs/normal.pdf",
)

binomial = DiscreteDistribution(
    "Binomial",
    params=[Param("Trial", "n", 10, lo=0),
            Param("P", "p", 0.5, lo=0, hi=1, increment=0.01)],
    k_param=Param("k", "k", 2, lo=0),
    pmf=lambda k, n, p: math.comb(int(n), int(k)) * p ** int(k)
        * (1 - p) ** (int(n) - int(k)),
    support=lambda n, p: np.arange(0, int(n) + 1, 1),
    a_default=4, b_default=2,
    info_pdf="pdfs/binomial.pdf",
)

levy = ContinuousDistribution(
    "Lévy",
    params=[Param("Location (μ)", "loc", 0),
            Param("Scale (c)", "scale", 1, lo=0)],
    pdf=lambda x, loc, scale: np.sqrt(scale / (2 * np.pi))
        * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2),
    plot_range=lambda loc, scale: (loc + 0.01, loc + 10),
    support=lambda loc, scale: (loc, np.inf),
    x_default=3, lo_default=1, hi_default=5, n_points=1000,
    info_pdf="pdfs/levey.pdf",
)

slash = ContinuousDistribution(
    "Slash",
    params=[],
    pdf=lambda x: _slash_pdf(x),
    plot_range=lambda: (-5, 5),
    support=lambda: (-np.inf, np.inf),
    x_default=1, lo_default=-1, hi_default=1, n_points=1000,
)

benini = ContinuousDistribution(
    "Benini",
    params=[Param("α (alpha)", "a", 4, lo=0, increment=0.1),
            Param("β (beta)", "b", 4, lo=0, increment=0.1),
            Param("σ (sigma)", "s", 4, lo=0.01, increment=0.1)],
    pdf=_benini_e,
    variants=[("ln (base e)", _benini_e), ("log (base 10)", _benini_10)],
    variant_label="Log Base",
    plot_range=lambda a, b, s: (0, 10),
    support=lambda a, b, s: (s, np.inf),
    x_default=5, lo_default=5, hi_default=7, n_points=500, axhline=True,
    le_note="\n \nPlease Note that the Benini distribution is only defined "
            "for P(X≤σ)  ",
    text_height=6,
)

reciprocal = ContinuousDistribution(
    "Reciprocal",
    params=[Param("a (support lower)", "a", 1, lo=0.01, increment=0.1),
            Param("b (support upper)", "b", 4, lo=0.01, increment=0.1)],
    pdf=lambda x, a, b: 1 / (x * (np.log(b) - np.log(a))),
    plot_range=lambda a, b: (a, b),
    support=lambda a, b: (a, b),
    x_default=2, lo_default=1.5, hi_default=3, n_points=1000,
)

raised_cosine = ContinuousDistribution(
    "Raised Cosine",
    params=[Param("μ (mean)", "u", 1, increment=0.1),
            Param("s (scale)", "s", 1, lo=0.01, increment=0.1)],
    pdf=lambda x, u, s: (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi)),
    plot_range=lambda u, s: (u - s, u + s),
    support=lambda u, s: (u - s, u + s),
    x_default=1, lo_default=0.5, hi_default=1.5, n_points=500,
)

kumaraswamy = ContinuousDistribution(
    "Kumaraswamy",
    params=[Param("a", "a", 10, lo=0.01, increment=0.1),
            Param("b", "b", 15, lo=0.01, increment=0.1)],
    pdf=lambda x, a, b: (a * b * x ** (a - 1)) * (1 - x ** a) ** (b - 1),
    plot_range=lambda a, b: (0, 1),
    support=lambda a, b: (0, 1),
    x_default=0.5, lo_default=0.3, hi_default=0.8, n_points=500,
)

cauchy = ContinuousDistribution(
    "Cauchy",
    params=[Param("Location (x₀)", "loc", 0),
            Param("Scale (γ)", "scale", 1, lo=0)],
    pdf=lambda x, loc, scale: 1 / (np.pi * scale * (1 + ((x - loc) / scale) ** 2)),
    plot_range=lambda loc, scale: (loc - 10 * scale, loc + 10 * scale),
    support=lambda loc, scale: (-np.inf, np.inf),
    x_default=0, lo_default=-1, hi_default=1, n_points=1000,
)

student_t = ContinuousDistribution(
    "Student's t",
    params=[Param("Degrees of freedom (ν)", "df", 5, lo=1)],
    pdf=lambda x, df: _t_pdf(x, df),
    plot_range=lambda df: (-8, 8),
    support=lambda df: (-np.inf, np.inf),
    x_default=0, lo_default=-1, hi_default=1, n_points=1000,
)

chi_squared = ContinuousDistribution(
    "Chi-squared",
    params=[Param("Degrees of freedom (k)", "k", 3, lo=1)],
    pdf=lambda x, k: _chi2_pdf(x, k),
    plot_range=lambda k: (0.001, k + 4 * np.sqrt(2 * k)),
    support=lambda k: (0, np.inf),
    x_default=1, lo_default=1, hi_default=4, n_points=1000,
)

bivariate_normal = SurfaceDistribution(
    "Bivariate Normal",
    params=[Param("μ (x)", "mean_x", 0), Param("μ (y)", "mean_y", 0),
            Param("σ (x)", "sd_x", 1, lo=0), Param("σ (y)", "sd_y", 1, lo=0),
            Param("ρ", "corr", 0.5, lo=-0.99, hi=0.99, increment=0.01)],
    surface=_binorm_surface,
)

bivariate_cauchy = SurfaceDistribution(
    "Bivariate Cauchy",
    params=[Param("Scale (x)", "scale_x", 1, lo=0),
            Param("Scale (y)", "scale_y", 1, lo=0),
            Param("Location (x)", "loc_x", 0),
            Param("Location (y)", "loc_y", 0),
            Param("ρ", "corr", 0.5, lo=-0.99, hi=0.99, increment=0.01)],
    surface=_bivariate_cauchy_surface,
)

dirichlet = SurfaceDistribution(
    "Dirichlet",
    params=[Param("α", "a", 2, lo=0), Param("β", "b", 3, lo=0)],
    surface=_dirichlet_surface,
)


# --------------------------------------------------------------------------- #
# Registry -- add a new distribution by appending one line here.              #
# --------------------------------------------------------------------------- #
DISTRIBUTIONS = {
    "Normal": normal,
    "Binomial": binomial,
    "Lévy": levy,
    "Slash": slash,
    "Benini": benini,
    "Reciprocal": reciprocal,
    "Raised Cosine": raised_cosine,
    "Kumaraswamy": kumaraswamy,
    "Cauchy": cauchy,
    "Student's t": student_t,
    "Chi-squared": chi_squared,
    "Bivariate Normal": bivariate_normal,
    "Bivariate Cauchy": bivariate_cauchy,
    "Dirichlet": dirichlet,
}
