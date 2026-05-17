# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:04:10 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def Raised_cos(ax, u=1, s=1):
    x = np.linspace(u - s, u + s, 500)
    y = (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))

    ax.plot(x, y)

def Raised_cos_left(ax, u=1, s=1, param=1):
    pdf = lambda x: (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))
    prob, _ = integrate.quad(pdf, u - s, param)

    x = np.linspace(u - s, u + s, 500)
    y = (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))

    x_fill = np.linspace(u - s, param, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Raised_cos_right(ax, u=1, s=1, param=1):
    pdf = lambda x: (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))
    prob, _ = integrate.quad(pdf, param, u + s)

    x = np.linspace(u - s, u + s, 500)
    y = (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))

    x_fill = np.linspace(param, u + s, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Raised_cos_between(ax, u=1, s=1, param1=0.5, param2=1.5):
    pdf = lambda x: (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(u - s, u + s, 500)
    y = (1 / (2 * s)) * (1 + np.cos(((x - u) / s) * np.pi))

    x_fill = np.linspace(param1, param2, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob
