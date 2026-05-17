# -*- coding: utf-8 -*-
"""
Created on Sun May 17 13:02:20 2026

@author: snaph
"""
import tkinter as tk
from tkinter import ttk

from Distributions.Binomial_dist import Bin_equal, Bin_left, Bin_right, Bin_between

def draw_normal(input_frame, fig, canvas):
    tk.Label(input_frame, text="Trial").pack()
    entry_trial = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="10"))
    entry_trial.pack()
    tk.Label(input_frame, text="P").pack()
    entry_p = tk.Spinbox(input_frame, from_=0, to=1, increment=0.01, textvariable=tk.StringVar(value="0.5"))
    entry_p.pack()
    tk.Label(input_frame, text="k").pack()
    entry_k = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="2"))
    entry_k.pack()

    combo_box = ttk.Combobox(input_frame, values=["P(X =k)", "P(X≤x)", "P(X≥x)", "P(a≤X≤b)"], state="readonly")
    combo_box.pack(pady=10)
    combo_box.set("P(X =k)")

    extra_frame = tk.Frame(input_frame)
    extra_frame.pack()
    
    def update_extra_inputs(event=None):
        for w in extra_frame.winfo_children():
            w.destroy()
        selection = combo_box.get()
        if selection == "P(a≤X≤b)":
            tk.Label(extra_frame, text="a (lower)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="2")).pack()
            tk.Label(extra_frame, text="b (upper)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="4")).pack()
        plot()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)
    
    text_widget = tk.Text(input_frame, height=2, width=20)
    text_widget.pack(pady=15)
    
    def plot():
        n = int(float(entry_trial.get()))
        p = float(entry_p.get())
        k = int(float(entry_k.get()))
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        if selection == "P(X =k)":
            Bin_equal(ax, n, k, p)
        elif selection == "P(X≤x)":
            prob = Bin_left(ax, n, k, p)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {k}) = {prob:.4f}")
        elif selection == "P(X≥x)":
            prob = Bin_right(ax, n, k, p)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {k}) = {prob:.4f}")
        elif selection == "P(a≤X≤b)":
            prob = Bin_between(ax, n, float(spinboxes[1].get()), float(spinboxes[0].get()), p)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
