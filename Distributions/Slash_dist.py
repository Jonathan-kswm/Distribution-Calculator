# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:10:52 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

_phi0 = 1 / np.sqrt(2 * np.pi)

def _pdf(x):
    if x == 0:
        return _phi0 / 2
    return _phi0 * (1 - np.exp(-0.5 * x**2)) / x**2

def _pdf_vec(x):
    with np.errstate(divide='ignore', invalid='ignore'):
        y = _phi0 * (1 - np.exp(-0.5 * x**2)) / x**2
    return np.where(x == 0, _phi0 / 2, y)

def Slash(ax):
    x = np.linspace(-5, 5, 1000)
    y = _pdf_vec(x)

    ax.plot(x, y)

def Slash_left(ax, param=0):
    prob, _ = integrate.quad(_pdf, -np.inf, param)

    x = np.linspace(-5, 5, 1000)
    y = _pdf_vec(x)

    x_fill = np.linspace(-5, param, 1000)
    y_fill = _pdf_vec(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Slash_right(ax, param=0):
    prob, _ = integrate.quad(_pdf, param, np.inf)

    x = np.linspace(-5, 5, 1000)
    y = _pdf_vec(x)

    x_fill = np.linspace(param, 5, 1000)
    y_fill = _pdf_vec(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Slash_between(ax, param1=-1, param2=1):
    prob, _ = integrate.quad(_pdf, param1, param2)

    x = np.linspace(-5, 5, 1000)
    y = _pdf_vec(x)

    x_fill = np.linspace(param1, param2, 1000)
    y_fill = _pdf_vec(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob
