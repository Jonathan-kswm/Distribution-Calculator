# -*- coding: utf-8 -*-
"""
Created on Sun May 17 12:09:15 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import math


def Bin_equal(ax, n=10, k=2, p=0.5):
    x = np.arange(0, n + 1, 1)
    y = []
    for i in x:
        yi = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (p**i) * (1-p)**(n-i)
        y.append(yi)

    bars = ax.bar(x, y)
    for idx, bar in enumerate(bars):
        if idx != k:
            bar.set_alpha(0.3)

    prob = (math.factorial(n) / (math.factorial(k) * math.factorial(n - k))) * (p**k) * (1-p)**(n-k)
    return prob


def Bin_left(ax, n=10, k=2, p=0.5):
    x = np.arange(0, n + 1, 1)
    y = []
    for i in x:
        yi = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (p**i) * (1-p)**(n-i)
        y.append(yi)

    bars = ax.bar(x, y)
    for idx, bar in enumerate(bars):
        if idx > k:
            bar.set_alpha(0.3)

    prob = sum(y[:k + 1])
    return prob

def Bin_right(ax, n=10, k=2, p=0.5):
    x = np.arange(0, n + 1, 1)
    y = []
    for i in x:
        yi = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (p**i) * (1-p)**(n-i)
        y.append(yi)

    bars = ax.bar(x, y)
    for idx, bar in enumerate(bars):
        if idx < k:
            bar.set_alpha(0.3)

    prob = sum(y[k:])
    return prob

def Bin_between(ax ,n =10, a  =2, b = 4, p=0.5):
    x = np.arange(0, n + 1, 1)
    y = []
    for i in x:
        yi = (math.factorial(n) / (math.factorial(i) * math.factorial(n - i))) * (p**i) * (1-p)**(n-i)
        y.append(yi)

    bars = ax.bar(x, y)
    for idx, bar in enumerate(bars):
        if idx < a:
            bar.set_alpha(0.3)
        elif idx > b:
            bar.set_alpha(0.3)
            
    prob = sum(y[a:b+1])
    return prob
