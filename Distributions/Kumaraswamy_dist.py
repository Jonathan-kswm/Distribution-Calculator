# -*- coding: utf-8 -*-
"""
Created on Sun May 17 23:10:35 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def Kuma(ax, a=10, b=15):
    x = np.linspace(0, 1, 500)
    y = (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)

    ax.plot(x, y)

def Kuma_left(ax, a=10, b=15, param=0.5):
    pdf = lambda x: (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)
    prob, _ = integrate.quad(pdf, 0, param)

    x = np.linspace(0, 1, 500)
    y = (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)

    x_fill = np.linspace(0, param, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Kuma_right(ax, a=10, b=15, param=0.5):
    pdf = lambda x: (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)
    prob, _ = integrate.quad(pdf, param, 1)

    x = np.linspace(0, 1, 500)
    y = (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)

    x_fill = np.linspace(param, 1, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Kuma_between(ax, a=10, b=15, param1=0.3, param2=0.8):
    pdf = lambda x: (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(0, 1, 500)
    y = (a * b * x**(a - 1)) * (1 - x**a)**(b - 1)

    x_fill = np.linspace(param1, param2, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob
