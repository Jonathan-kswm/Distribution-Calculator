import tkinter as tk
from tkinter import ttk

from Distributions.Raised_cosine_dist import Raised_cos, Raised_cos_left, Raised_cos_right, Raised_cos_between


def draw_raised_cosine(input_frame, fig, canvas):
    tk.Label(input_frame, text="μ (mean)").pack()
    entry_u = tk.Spinbox(input_frame, from_=-1000, to=1000, increment=0.1, textvariable=tk.StringVar(value="1"))
    entry_u.pack()
    tk.Label(input_frame, text="s (scale)").pack()
    entry_s = tk.Spinbox(input_frame, from_=0.01, to=1000, increment=0.1, textvariable=tk.StringVar(value="1"))
    entry_s.pack()

    combo_box = ttk.Combobox(input_frame, values=["Curve", "P(X≤x)", "P(X≥x)", "P(a≤X≤b)"], state="readonly")
    combo_box.pack(pady=10)
    combo_box.set("Curve")

    extra_frame = tk.Frame(input_frame)
    extra_frame.pack()

    def update_extra_inputs(event=None):
        for w in extra_frame.winfo_children():
            w.destroy()
        selection = combo_box.get()
        if selection in ("P(X≤x)", "P(X≥x)"):
            tk.Label(extra_frame, text="x").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, increment=0.1, textvariable=tk.StringVar(value="1")).pack()
        elif selection == "P(a≤X≤b)":
            tk.Label(extra_frame, text="a (lower)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, increment=0.1, textvariable=tk.StringVar(value="0.5")).pack()
            tk.Label(extra_frame, text="b (upper)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, increment=0.1, textvariable=tk.StringVar(value="1.5")).pack()
        plot()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)

    text_widget = tk.Text(input_frame, height=2, width=20)
    text_widget.pack(pady=15)

    def plot():
        u = float(entry_u.get())
        s = float(entry_s.get())
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        if selection == "Curve":
            Raised_cos(ax, u=u, s=s)
        elif selection == "P(X≤x)":
            prob = Raised_cos_left(ax, u=u, s=s, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {float(spinboxes[0].get())}) = {prob:.4f}")
        elif selection == "P(X≥x)":
            prob = Raised_cos_right(ax, u=u, s=s, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {float(spinboxes[0].get())}) = {prob:.4f}")
        elif selection == "P(a≤X≤b)":
            prob = Raised_cos_between(ax, u=u, s=s, param1=float(spinboxes[0].get()), param2=float(spinboxes[1].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
