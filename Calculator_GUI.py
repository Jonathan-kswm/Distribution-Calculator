# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import subprocess
import sys
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Panels.normal_panel import draw_normal
from Panels.bivariate_panel import draw_bivariate
from Panels.Binomial_panel import draw_normal as draw_binomial
from Panels.Levy_panel import draw_levy
from Panels.Slash_panel import draw_slash
from Panels.Benini_panel import draw_benini
from Panels.Reciprocal_panel import draw_reciprocal
from Panels.Raised_cosine_panel import draw_raised_cosine
from Panels.Kumaraswamy_panel import draw_kumaraswamy

def open_new_window():
    subprocess.Popen([sys.executable, __file__])


root = tk.Tk()
root.title("Distribution Calculator")
root.geometry("1200x500")
root.minsize(1100, 400)

#---file menue---
menu = tk.Menu(root)
root.config(menu=menu)

filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_command(label="Open...")

windowmenu = tk.Menu(menu)
menu.add_cascade(label="Window", menu=windowmenu)
windowmenu.add_command(label="New Window", command=open_new_window)


helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")

# ---Left panel: scrollbar + listbox---
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(left_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

Mylist = tk.Listbox(left_frame, yscrollcommand=scrollbar.set)
Mylist.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=Mylist.yview)

# ---Right panel: inputs---
input_frame = tk.Frame(root, width= 200, padx=10, pady=10)
input_frame.pack_propagate(False)
input_frame.pack(side=tk.RIGHT, fill=tk.Y)

# ---Centre panel: canvas---
right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

fig = plt.figure()
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def reset_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()


# ---Distribution registry---
# To add a new distribution: write a draw function in Panels/ and register it here.
DISTRIBUTIONS = {
    "Normal": draw_normal,
    "Binomial": draw_binomial,
    "Lévy": draw_levy,
    "Slash": draw_slash,
    "Benini": draw_benini,
    "Reciprocal": draw_reciprocal,
    "Raised Cosine": draw_raised_cosine,
    "Kumaraswamy": draw_kumaraswamy,
    "Bivariate Normal": draw_bivariate,
}

for name in DISTRIBUTIONS:
    Mylist.insert(tk.END, name)

current_distribution = "Normal"

def on_select(event):
    selection = Mylist.curselection()
    if not selection:
        return
    choice = Mylist.get(selection[0])
    if choice in DISTRIBUTIONS:
        current_distribution = choice
        reset_inputs()
        DISTRIBUTIONS[choice](input_frame, fig, canvas)

def info(current_distribution):
    new_window = tk.Toplevel(root)
    new_window.title("New Window")
    new_window.geometry("300x200")
    label = tk.Label(new_window, text="This is a new window!")
    label.pack(pady=20)
    
infomenu = tk.Menu(menu)
menu.add_cascade(label="Info", menu=infomenu)
infomenu.add_command(label="About", command=info(current_distribution))

Mylist.bind("<<ListboxSelect>>", on_select)

reset_inputs()
draw_normal(input_frame, fig, canvas)
root.mainloop()
