# -*- coding: utf-8 -*-
"""
Created on Thu May 21 00:24:47 2026

@author: snaph
"""
import tkinter as tk
from tkinter import ttk

from Distributions.Bivariate_Cauchy_dist import standard_bivariate_cauchy, bivariate_cauchy

def draw_bivariate_cauchy(input_frame, fig, canvas):
    combo_box = ttk.Combobox(input_frame, values=["Standard", "Interactive"], state="readonly")
    combo_box.pack(pady=10)
    combo_box.set("Standard")
    
    extra_frame = tk.Frame(input_frame)
    extra_frame.pack()
    
    def update_extra_inputs(event=None):
        for w in extra_frame.winfo_children():
            w.destroy()
        selection = combo_box.get()
        if selection == "Interactive":
            tk.Label(extra_frame, text="Scale (x)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1")).pack()
             
            tk.Label(extra_frame, text="Scale (y)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1")).pack()
            
            tk.Label(extra_frame, text="Location (x)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0")).pack()
                        
            tk.Label(extra_frame, text="Location (y)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0")).pack()
                        
            tk.Label(extra_frame, text="ρ").pack()
            tk.Spinbox(extra_frame, from_=-0.99, to=0.99, textvariable=tk.StringVar(value="0.5")).pack()
        else: #selection == "Standard":
            pass #this may need to be changed
        plot()
    
    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)
    
    #to be used later:
    text_widget = tk.Text(input_frame, height=6, width=20)
    text_widget.pack(pady=15)
    
    view = tk.StringVar(value="3D")
    check_3d = tk.BooleanVar(value=True)
    check_XZ = tk.BooleanVar(value=False)
    check_YZ = tk.BooleanVar(value=False)
    check_XY = tk.BooleanVar(value=False)
    
    def select_3d():
        view.set("3D")
        check_3d.set(value=True)
        check_XZ.set(value=False)
        check_YZ.set(value=False)
        check_XY.set(value=False)        
        
    def select_XZ():
        view.set("XZ")
        check_3d.set(value=False)
        check_XZ.set(value=True)
        check_YZ.set(value=False)
        check_XY.set(value=False)
        
    def select_YZ():
        view.set("YZ")
        check_3d.set(value=False)
        check_XZ.set(value=False)
        check_YZ.set(value=True)
        check_XY.set(value=False)

    def select_XY():        
        view.set("XY")
        check_3d.set(value=False)
        check_XZ.set(value=False)
        check_YZ.set(value=False)
        check_XY.set(value=True)
    
    tk.Label(input_frame, text="View:").pack()
    tk.Checkbutton(input_frame, text="3D", variable=check_3d, command=select_3d).pack()
    tk.Checkbutton(input_frame, text="XZ", variable=check_XZ, command=select_XZ).pack()
    tk.Checkbutton(input_frame, text="YZ", variable=check_YZ, command=select_YZ).pack()
    tk.Checkbutton(input_frame, text="XY", variable=check_XY, command=select_XY).pack()


    def plot():
        rotation = view.get()
        fig.clear()
        ax = fig.add_subplot(111, projection="3d")
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        
        if selection == "Standard":
                if rotation == "3D":
                    standard_bivariate_cauchy(ax)
                    canvas.draw()
                elif rotation == "XY":
                    ax.set_proj_type('ortho')
                    ax.view_init(elev= 90, azim= -90, roll= 0)
                    standard_bivariate_cauchy(ax)
                    canvas.draw()
                elif rotation == "XZ":
                    ax.set_proj_type('ortho')
                    ax.view_init(elev= 0, azim= -90, roll= 0)
                    standard_bivariate_cauchy(ax)
                    canvas.draw()
                elif rotation == "YZ":
                    ax.set_proj_type('ortho')
                    ax.view_init(elev= 0, azim= 0, roll= 0)
                    standard_bivariate_cauchy(ax)
                    canvas.draw()
        elif selection == "Interactive":
            if rotation == "3D":
                bivariate_cauchy(ax, float(spinboxes[0].get()), float(spinboxes[1].get()), float(spinboxes[2].get()), float(spinboxes[3].get()), float(spinboxes[4].get()))
                canvas.draw()
            elif rotation == "XY":
                ax.set_proj_type('ortho')
                ax.view_init(elev= 90, azim= -90, roll= 0)
                bivariate_cauchy(ax, float(spinboxes[0].get()), float(spinboxes[1].get()), float(spinboxes[2].get()), float(spinboxes[3].get()), float(spinboxes[4].get()))
                canvas.draw()
            elif rotation == "XZ":
                ax.set_proj_type('ortho')
                ax.view_init(elev= 0, azim= -90, roll= 0)
                bivariate_cauchy(ax, float(spinboxes[0].get()), float(spinboxes[1].get()), float(spinboxes[2].get()), float(spinboxes[3].get()), float(spinboxes[4].get()))
                canvas.draw()
            elif rotation == "YZ":
                ax.set_proj_type('ortho')
                ax.view_init(elev= 0, azim= 0, roll= 0)
                bivariate_cauchy(ax, float(spinboxes[0].get()), float(spinboxes[1].get()), float(spinboxes[2].get()), float(spinboxes[3].get()), float(spinboxes[4].get()))
                canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()