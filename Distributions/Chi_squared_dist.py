# -*- coding: utf-8 -*-
"""
Created on Fri May 22 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

from scipy.special import gamma


def chi2_pdf(x, k):
    return (1.0 / (2**(k / 2) * gamma(k / 2))) * x**(k / 2 - 1) * np.exp(-x / 2)


def _upper(k):
    return k + 4 * np.sqrt(2 * k)


def chi_squared(ax, df = 3):
    x = np.linspace(0.001, _upper(df), 1000)
    y = chi2_pdf(x, df)

    ax.plot(x, y)


def chi_squared_left(ax, df = 3, param = 1):
    pdf = lambda x: chi2_pdf(x, df)
    prob, _ = integrate.quad(pdf, 0, param)

    x = np.linspace(0.001, _upper(df), 1000)
    y = pdf(x)

    x_fill = np.linspace(0.001, param, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob


def chi_squared_right(ax, df = 3, param = 1):
    pdf = lambda x: chi2_pdf(x, df)
    prob, _ = integrate.quad(pdf, param, np.inf)

    x = np.linspace(0.001, _upper(df), 1000)
    y = pdf(x)

    x_fill = np.linspace(param, _upper(df), 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob


def chi_squared_between(ax, df = 3, param1 = 1, param2 = 4):
    pdf = lambda x: chi2_pdf(x, df)
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(0.001, _upper(df), 1000)
    y = pdf(x)

    x_fill = np.linspace(param1, param2, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob
