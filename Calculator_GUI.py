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

root = tk.Tk()
root.title("Distribution Calculator")
root.geometry("800x500")

# ---Left panel: scrollbar + listbox---
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

Mylist = tk.Listbox(left_frame, yscrollcommand=scrollbar.set)
Mylist.insert(tk.END, "Normal", "Multivariate Normal")
Mylist.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=Mylist.yview)

# ---Right panel: canvas---
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

fig, ax = plt.subplots()
x = np.linspace(-4, 4, 500)
ax.plot(x, (1/np.sqrt(2*np.pi))*np.exp(-0.5*x**2))

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# ---Buttons---
btn = tk.Button(root, text="Calculate", command=lambda: print("Calculate clicked"))
btn2 = tk.Button(root, text="Calculate", command=lambda: print("yay"))
btn.pack(side=tk.BOTTOM, pady=10)
btn2.pack(side=tk.BOTTOM, pady=10)

root.mainloop()
