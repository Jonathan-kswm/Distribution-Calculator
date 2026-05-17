# -*- coding: utf-8 -*-
"""
Created on Sun May 17 22:49:24 2026

@author: snaph
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def Reciprocal(ax, a=1, b=4):
    x = np.linspace(a, b, 1000)
    y = 1 / (x * (np.log(b) - np.log(a)))

    ax.plot(x, y)

def Reciprocal_left(ax, a=1, b=4, param=2):
    pdf = lambda x: 1 / (x * (np.log(b) - np.log(a)))
    prob, _ = integrate.quad(pdf, a, param)

    x = np.linspace(a, b, 1000)
    y = 1 / (x * (np.log(b) - np.log(a)))

    x_fill = np.linspace(a, param, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Reciprocal_right(ax, a=1, b=4, param=2):
    pdf = lambda x: 1 / (x * (np.log(b) - np.log(a)))
    prob, _ = integrate.quad(pdf, param, b)

    x = np.linspace(a, b, 1000)
    y = 1 / (x * (np.log(b) - np.log(a)))

    x_fill = np.linspace(param, b, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob

def Reciprocal_between(ax, a=1, b=4, param1=1.5, param2=3):
    pdf = lambda x: 1 / (x * (np.log(b) - np.log(a)))
    prob, _ = integrate.quad(pdf, param1, param2)

    x = np.linspace(a, b, 1000)
    y = 1 / (x * (np.log(b) - np.log(a)))

    x_fill = np.linspace(param1, param2, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)

    ax.plot(x, y)
    return prob
