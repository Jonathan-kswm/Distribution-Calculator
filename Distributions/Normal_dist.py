# -*- coding: utf-8 -*-
"""
Created on Sun May 17 07:18:17 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np

def N(mean = 0, sd = 1):
    x = np.linspace(mean - 4*sd, mean + 4*sd, 500)
    y = (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)

    plt.plot(x, y)
    plt.show()