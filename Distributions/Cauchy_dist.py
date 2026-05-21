# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:59:46 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def cau(ax, loc = 0, scale = 1):
    x = np.linspace(loc - 10*scale, loc + 10*scale, 1000)
    y = 1 / (np.pi * scale * (1 + ((x - loc) / scale)**2))

    ax.plot(x, y)

def cau_left(ax, loc = 0, scale = 1, param = 1):
    pdf = lambda x: 1 / (np.pi * scale * (1 + ((x - loc) / scale)**2))
    prob, _ = integrate.quad(pdf, -np.inf, param)

    x = np.linspace(loc - 10*scale, loc + 10*scale, 1000)
    y = pdf(x)

    x_fill = np.linspace(loc - 10*scale, param, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob

def cau_right(ax, loc = 0, scale = 1, param = 1):
    pdf = lambda x: 1 / (np.pi * scale * (1 + ((x - loc) / scale)**2))
    prob, _ = integrate.quad(pdf, param, np.inf)

    x = np.linspace(loc - 10*scale, loc + 10*scale, 1000)
    y = pdf(x)

    x_fill = np.linspace(param, loc + 10*scale, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob

def cau_between(ax, loc = 0, scale = 1, param1 = -1, param2 = 1):
    pdf = lambda x: 1 / (np.pi * scale * (1 + ((x - loc) / scale)**2))
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(loc - 10*scale, loc + 10*scale, 1000)
    y = pdf(x)

    x_fill = np.linspace(param1, param2, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)

    ax.plot(x, y)
    return prob
