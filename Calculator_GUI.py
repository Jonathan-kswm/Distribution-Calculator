# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Panels.normal_panel import draw_normal
from Panels.bivariate_panel import draw_bivariate
from Panels.Binomial_panel import draw_normal as draw_binomial

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

# ---Centre panel: canvas---
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=False)

# ---Right panel: inputs---
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.Y)


def reset_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()


# ---Distribution registry---
# To add a new distribution: write a draw function in Panels/ and register it here.
DISTRIBUTIONS = {
    "Normal": draw_normal,
    "Bivariate Normal": draw_bivariate,
    "Binomial": draw_binomial,
}

for name in DISTRIBUTIONS:
    Mylist.insert(tk.END, name)


def on_select(event):
    selection = Mylist.curselection()
    if not selection:
        return
    choice = Mylist.get(selection[0])
    if choice in DISTRIBUTIONS:
        reset_inputs()
        DISTRIBUTIONS[choice](input_frame, fig, canvas)


Mylist.bind("<<ListboxSelect>>", on_select)

reset_inputs()
draw_normal(input_frame, fig, canvas)
root.mainloop()
