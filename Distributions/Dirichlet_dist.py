# -*- coding: utf-8 -*-
"""
Created on Thu May 21 02:39:19 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator
from scipy.integrate import quad

def dirichlet(ax, a = 2, b = 3):
    x = np.arange(0, 1, 0.01)
    y = np.arange(0, 1, 0.01)

    x,y = np.meshgrid(x,y)

    def gamma_integrand(t, z):
        return (t**(z -1))*(np.exp(-t))

    def gamma(z):
        return quad(gamma_integrand, 0, np.inf, args = z)[0]

    def B(a, b):
        numerator = gamma(a)*gamma(b)
        denominator = gamma( a + b)
        return numerator/denominator

    z = (B(a, b)**-1)*(x**(a -1)*y**(b -1))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Prob")
    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=True)
    ax.set_zlim(0, 1.5*z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')