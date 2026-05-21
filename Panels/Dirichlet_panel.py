import tkinter as tk
from tkinter import ttk

from Distributions.Dirichlet_dist import dirichlet


def draw_dirichlet(input_frame, fig, canvas):
    tk.Label(input_frame, text="α").pack()
    entry_a = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="2"))
    entry_a.pack()

    tk.Label(input_frame, text="β").pack()
    entry_b = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="3"))
    entry_b.pack()

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

        if rotation == "3D":
            dirichlet(ax, float(entry_a.get()), float(entry_b.get()))
            canvas.draw()
        elif rotation == "XY":
            ax.set_proj_type('ortho')
            ax.view_init(elev= 90, azim= -90, roll= 0)
            dirichlet(ax, float(entry_a.get()), float(entry_b.get()))
            canvas.draw()
        elif rotation == "XZ":
            ax.set_proj_type('ortho')
            ax.view_init(elev= 0, azim= -90, roll= 0)
            dirichlet(ax, float(entry_a.get()), float(entry_b.get()))
            canvas.draw()
        elif rotation == "YZ":
            ax.set_proj_type('ortho')
            ax.view_init(elev= 0, azim= 0, roll= 0)
            dirichlet(ax, float(entry_a.get()), float(entry_b.get()))
            canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
