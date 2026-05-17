# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:09:34 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def lev(ax, x = 2, loc = 1, scale = 2):
    x = np.linspace(loc + 0.01, loc + 10, 1000)
    y = np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    
    ax.plot(x,y)
    
def lev_left(ax, x = 2, loc =1, scale = 2, param = 3):
    pdf = lambda x: np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    prob, _ = integrate.quad(pdf, loc, param)
    
    x = np.linspace(loc + 0.01, loc + 10, 1000)
    y = np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    
    x_fill = np.linspace(loc + 0.01, param, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)
    
    ax.plot(x,y)
    return prob

def lev_right(ax, x = 2, loc =1, scale = 2, param = 3):
    pdf = lambda x: np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    prob, _ = integrate.quad(pdf, param, np.inf)
    
    x = np.linspace(loc + 0.01, loc + 10, 1000)
    y = np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    
    x_fill = np.linspace(param, loc + 10, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)
    
    ax.plot(x,y)
    return prob

def lev_between(ax, x = 2, loc =1, scale = 2, param1 = 3, param2 = 5):
    pdf = lambda x: np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    prob, _ = integrate.quad(pdf, param1, param2)
    
    x = np.linspace(loc + 0.01, loc + 10, 1000)
    y = np.sqrt(scale / (2 * np.pi)) * np.exp(-scale / (2 * (x - loc))) / (x - loc) ** (3 / 2)
    
    x_fill = np.linspace(param1, param2, 1000)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha = 0.4)
    
    ax.plot(x,y)
    return prob