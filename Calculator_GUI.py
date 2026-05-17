# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Distributions.Normal_dist import N_left, N_right, N_dual
from Distributions.Multivariate_normal import binorm

root = tk.Tk()
root.title("Distribution Calculator")
root.geometry("800x500")

# ---Left panel: scrollbar + listbox---
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

Mylist = tk.Listbox(left_frame, yscrollcommand=scrollbar.set)
Mylist.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=Mylist.yview)

# ---Right panel: canvas---
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig = plt.figure()

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---Distribution draw functions---
# To add a new distribution: write a draw function and add it to DISTRIBUTIONS.

def draw_normal():
    fig.clear()
    ax = fig.add_subplot(111)
    x = np.linspace(-4, 4, 500)
    ax.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-0.5*x**2))
    canvas.draw()

def draw_bivariate():
    fig.clear()
    ax = fig.add_subplot(111, projection='3d')
    binorm(ax)
    canvas.draw()

DISTRIBUTIONS = {
    "Normal": draw_normal,
    "Bivariate Normal": draw_bivariate,
}

for name in DISTRIBUTIONS:
    Mylist.insert(tk.END, name)

def on_select(event):
    selection = Mylist.curselection()
    if not selection:
        return
    choice = Mylist.get(selection[0])
    if choice in DISTRIBUTIONS:
        DISTRIBUTIONS[choice]()

Mylist.bind("<<ListboxSelect>>", on_select)

draw_normal()

# ---Buttons---
btn = tk.Button(root, text="Calculate", command=lambda: print("Calculate clicked"))
btn2 = tk.Button(root, text="Calculate", command=lambda: print("yay"))
btn.pack(side=tk.BOTTOM, pady=10)
btn2.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
