# -*- coding: utf-8 -*-
"""
Created on Sun May 17 06:25:04 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

mean = (0, 0)

var_x = 1
var_y = 1
corr_x_y = 0.5

Sigma = ((var_x**2, corr_x_y*var_x*var_y),
         (corr_x_y*var_x*var_y, var_y**2))

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)

X, Y = np.meshgrid(X, Y)

R = ((X-mean[0])/var_x)**2 - 2*corr_x_y*((X - mean[0])/var_x)*((Y-mean[1])/var_y) + ((Y-mean[1])/var_y)**2
Z = (1/(2*np.pi*var_x*var_y*np.sqrt(1-corr_x_y**2)))*np.exp((-1/(2*(1-corr_x_y**2))) * R)

surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

ax.set_zlim(0, 1.0)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()