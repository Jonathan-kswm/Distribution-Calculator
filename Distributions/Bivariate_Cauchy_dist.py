# -*- coding: utf-8 -*-
"""
Created on Wed May 20 22:45:51 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import cm
from matplotlib.ticker import LinearLocator

#f(x,y)=2π1​(1+x2+y2)−3/2

#f(x,y)=2πγx​γy​1−ρ2​1​(1+1−ρ21​[γx2​(x−μx​)2​−γx​γy​2ρ(x−μx​)(y−μy​)​+γy2​(y−μy​)2​])−3/2

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

def standard_bivariate_cauchy(ax):
    x = np.arange(-3, 3, 0.1)
    y = np.arange(-3, 3, 0.1)
    
    x, y = np.meshgrid(x, y)
    
    z = ( 1 / (2*np.pi)) * (1 + x**2 + y**2)**(-3/2)
    
    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth= 0, antialiased = True)
    ax.set_zlim(0, 1.5*z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    
def bivariate_cauchy(ax, scale_x = 1, scale_y = 1, loc_x = 0, loc_y = 0, corr = 0.5):
    x = np.arange(loc_x - 4*scale_x, loc_x + 4*scale_x, 0.1)
    y = np.arange(loc_y - 4*scale_y, loc_y + 4*scale_y, 0.1)
    
    x, y = np.meshgrid(x,y)
    
    z = (1 / (2 * np.pi * scale_x * scale_y * np.sqrt(1 - corr**2))) * ( 1 + (1 / (1 - corr**2)) * ( ((x - loc_x)**2 / scale_x**2) - ((2 * corr * (x - loc_x) * ( y - loc_y))/(scale_x*scale_y)) + ((y - loc_y)**2)/scale_y**2))**(-3/2)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Prob")
    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth= 0, antialiased = True)
    ax.set_zlim(0, 1.5*z.max())
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter('{x:.02f}')
    

    
    
