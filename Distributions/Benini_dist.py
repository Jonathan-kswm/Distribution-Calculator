# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:32:04 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def Benini10(ax, a=4, b=4, s=4):
    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)

def Benini10_left(ax, a=4, b=4, s=4, param=5):
    pdf = lambda x: np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)
    prob, _ = integrate.quad(pdf, s, param)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)

    x_fill = np.linspace(s, param, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob

def Benini10_right(ax, a=4, b=4, s=4, param=5):
    pdf = lambda x: np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)
    prob, _ = integrate.quad(pdf, param, np.inf)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)

    x_fill = np.linspace(param, 10, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob

def Benini10_between(ax, a=4, b=4, s=4, param1=5, param2=7):
    pdf = lambda x: np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log10(x/s) - b * (np.log10(x/s))**2) * (a/x + (2 * b * np.log10(x/s))/x)

    x_fill = np.linspace(param1, param2, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob

def Benini_e(ax, a=4, b=4, s=4):
    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)

def Benini_e_left(ax, a=4, b=4, s=4, param=5):
    pdf = lambda x: np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)
    prob, _ = integrate.quad(pdf, s, param)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)

    x_fill = np.linspace(s, param, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob

def Benini_e_right(ax, a=4, b=4, s=4, param=5):
    pdf = lambda x: np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)
    prob, _ = integrate.quad(pdf, param, np.inf)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)

    x_fill = np.linspace(param, 10, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob

def Benini_e_between(ax, a=4, b=4, s=4, param1=5, param2=7):
    pdf = lambda x: np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(0, 10, 500)
    y = np.exp(-a * np.log(x/s) - b * (np.log(x/s))**2) * (a/x + (2 * b * np.log(x/s))/x)

    x_fill = np.linspace(param1, param2, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.axhline(0, color='black', linewidth=0.5)
    ax.plot(x, y)
    return prob
