# -*- coding: utf-8 -*-
"""
Created on Sun May 17 07:18:17 2026

@author: snaph
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate

def N(ax, mean = 0, sd = 1):
    x = np.linspace(mean - 4*sd, mean + 4*sd, 500)
    y = (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)

    ax.plot(x, y)

def N_left(ax, mean = 0, sd = 1, X = 1):
    pdf = lambda x: (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    prob_X, _ = integrate.quad(pdf, -np.inf, X)
    
    x = np.linspace(mean - 4*sd, mean + 4*sd, 500)
    y = (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    
    x_fill = np.linspace(mean - 4*sd, X, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)
    
    #ax.annotate(f"P(X ≤ {X}) = {prob_X:.2f}", xy= (max(x)-1.8, max(y)))
    
    ax.plot(x, y)
    return prob_X

def N_right(ax, mean = 0, sd = 1, X = 1):
    pdf = lambda x: (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    prob_X, _ = integrate.quad(pdf, X, np.inf)
    
    x = np.linspace(mean - 4*sd, mean + 4*sd, 500)
    y = (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    
    x_fill = np.linspace(X, mean + 4*sd, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)
    
    #ax.annotate(f"P(X ≥ {X}) = {prob_X:.2f}", xy= (max(x)-1.8, max(y)))

    ax.plot(x, y)
    return prob_X

def N_dual(ax, mean = 0, sd = 1, X1 = 0.25, X2 = -0.25):
    pdf = lambda x: (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    prob_X, _ = integrate.quad(pdf, X2, X1)
    
    x = np.linspace(mean - 4*sd, mean + 4*sd, 500)
    y = (1/(np.sqrt(2*np.pi)*sd))*np.exp(-0.5*((x-mean)/sd)**2)
    
    x_fill = np.linspace(X2, X1, 500)
    y_fill = pdf(x_fill)
    ax.fill_between(x_fill, y_fill, alpha=0.4)
    
    #ax.annotate(f"P( {X1}≥ X ≥ {X2}) = {prob_X:.2f}", xy= (max(x)-3.3, max(y)))

    ax.plot(x, y)
    return prob_X


    
    