# -*- coding: utf-8 -*-
"""
Created on Fri May 22 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

from scipy.special import gamma


def t_pdf(x, df):
    return gamma((df + 1) / 2) / (np.sqrt(df * np.pi) * gamma(df / 2)) * (1 + x**2 / df)**(-(df + 1) / 2)


def student_t(ax, df = 5):
    x = np.linspace(-8, 8, 1000)
    y = t_pdf(x, df)

    ax.plot(x, y)


def student_t_left(ax, df = 5, param = 1):
    pdf = lambda x: t_pdf(x, df)
    prob, _ = integrate.quad(pdf, -np.inf, param)

    x = np.linspace(-8, 8, 1000)
    y = pdf(x)

    x_fill = np.linspace(-8, param, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob


def student_t_right(ax, df = 5, param = 1):
    pdf = lambda x: t_pdf(x, df)
    prob, _ = integrate.quad(pdf, param, np.inf)

    x = np.linspace(-8, 8, 1000)
    y = pdf(x)

    x_fill = np.linspace(param, 8, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob


def student_t_between(ax, df = 5, param1 = -1, param2 = 1):
    pdf = lambda x: t_pdf(x, df)
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(-8, 8, 1000)
    y = pdf(x)

    x_fill = np.linspace(param1, param2, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob
