# -*- coding: utf-8 -*-
"""
Created on Sun May 17 06:25:04 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

def binorm(ax, mean_x=0, mean_y=0, var_x=1, var_y=1, corr_x_y=0.5):
    Sigma = ((var_x**2, corr_x_y*var_x*var_y),
             (corr_x_y*var_x*var_y, var_y**2))

    X = np.arange(mean_x - 3*var_x, mean_x + 3*var_x, 0.25)
    Y = np.arange(mean_y - 3*var_y, mean_y + 3*var_y, 0.25)

    X, Y = np.meshgrid(X, Y)

    R = ((X-mean_x)/var_x)**2 - 2*corr_x_y*((X - mean_x)/var_x)*((Y-mean_y)/var_y) + ((Y-mean_y)/var_y)**2
    Z = (1/(2*np.pi*var_x*var_y*np.sqrt(1-corr_x_y**2)))*np.exp((-1/(2*(1-corr_x_y**2))) * R)

    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    ax.set_zlim(0, 1.5*Z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')

    return Sigma