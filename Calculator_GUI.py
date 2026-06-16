# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import subprocess
import sys
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PDF_reader import show_pdf
import datetime

from New_Distributions import DISTRIBUTIONS

def open_new_window():
    subprocess.Popen([sys.executable, __file__])

root = tk.Tk()
root.title("Distribution Calculator")
root.geometry("1200x800")
root.minsize(1100, 400)

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
# To add a new distribution: define a spec in New_Distributions.py and add it
# to the DISTRIBUTIONS dict there. Nothing in this file needs to change.

for name in DISTRIBUTIONS:
    Mylist.insert(tk.END, name)

global current_distribution
current_distribution = "Normal"

def on_select(event):
    selection = Mylist.curselection()
    if not selection:
        return
    choice = Mylist.get(selection[0])
    if choice in DISTRIBUTIONS:
        global current_distribution
        current_distribution = choice
        reset_inputs()
        DISTRIBUTIONS[choice].draw(input_frame, fig, canvas)

def info(current_distribution = current_distribution):
    new_window = tk.Toplevel(root)
    new_window.title(f"{current_distribution}")
    new_window.geometry("600x800")
    pdf =  show_pdf(new_window, DISTRIBUTIONS[current_distribution].info_pdf)
    #pdf = tk.Canvas(new_window, image=show_pdf(new_window, "normal.pdf"))
    pdf.pack(pady=20)
    

    
def save_figure(current_distribution):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = filedialog.asksaveasfilename(
        defaultextension=".png",
        initialfile=f"{current_distribution}_{timestamp}.png",
        filetypes=[("PNG image", "*.png"), ("PDF", "*.pdf"), ("SVG", "*.svg"), ("All files", "*.*")],
        title="Save figure as",
    )
    if path:
        canvas.figure.savefig(path)

#---file menue---
menu = tk.Menu(root)
root.config(menu=menu)

filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
#filemenu.add_command(label="New")
#filemenu.add_command(label="Open...")
filemenu.add_command(label="Save", command= lambda: save_figure(current_distribution))

windowmenu = tk.Menu(menu)
menu.add_cascade(label="Window", menu=windowmenu)
windowmenu.add_command(label="New Window", command=open_new_window)

#helpmenu = tk.Menu(menu)
#menu.add_cascade(label="Help", menu=helpmenu)
#helpmenu.add_command(label="About")
    
infomenu = tk.Menu(menu)
menu.add_cascade(label="Info", menu=infomenu)
infomenu.add_command(label="About", command= lambda: info(current_distribution))

Mylist.bind("<<ListboxSelect>>", on_select)

reset_inputs()
DISTRIBUTIONS["Normal"].draw(input_frame, fig, canvas)
root.mainloop()

#while True:
#    print(current_distribution)
    
