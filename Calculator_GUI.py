# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Distributions.Normal_dist import N, N_left, N_right, N_dual
from Distributions.Multivariate_normal import binorm

root = tk.Tk()
root.title("Distribution Calculator")
root.geometry("1200x500")

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
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

fig = plt.figure()

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)


# ---Right panel: inputs---
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)
# ---Distribution draw functions---
# To add a new distribution: write a draw function and add it to DISTRIBUTIONS.

def draw_normal():
    tk.Label(input_frame, text="Mean").pack()
    entry1 = tk.Spinbox(input_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0"))
    entry1.pack()
    tk.Label(input_frame, text="SD").pack()
    entry2 = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1"))
    entry2.pack()

    def plot():
        mean = float(entry1.get())
        sd = float(entry2.get())
        fig.clear()
        ax = fig.add_subplot(111)
        N(ax, mean, sd)
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
    
    
    
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
root.mainloop()




