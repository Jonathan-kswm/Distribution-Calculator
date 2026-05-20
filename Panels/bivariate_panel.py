import tkinter as tk
from tkinter import ttk

from Distributions.Multivariate_normal import binorm


def draw_bivariate(input_frame, fig, canvas):
    tk.Label(input_frame, text="μ (x)").pack()
    entry_mean_x = tk.Spinbox(input_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0"))
    entry_mean_x.pack()
     
    tk.Label(input_frame, text="μ (y)").pack()
    entry_mean_y = tk.Spinbox(input_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0"))
    entry_mean_y.pack()
    
    tk.Label(input_frame, text="σ (x)").pack()
    entry_sd_x = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1"))
    entry_sd_x.pack()
    
    tk.Label(input_frame, text="σ (y)").pack()
    entry_sd_y = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1"))
    entry_sd_y.pack()
    
    tk.Label(input_frame, text="ρ").pack()
    entry_corr = tk.Spinbox(input_frame, from_=-0.99, to=0.99, textvariable=tk.StringVar(value="0.5"))
    entry_corr.pack()

    def plot():
        fig.clear()
        ax = fig.add_subplot(111, projection="3d")
        binorm(ax, float(entry_mean_x.get()), float(entry_mean_y.get()), float(entry_sd_x.get()), float(entry_sd_y.get()), float(entry_corr.get()))
        canvas.draw()
    
    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
