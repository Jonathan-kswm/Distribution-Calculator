import tkinter as tk
from tkinter import ttk

from Distributions.Normal_dist import N, N_left, N_right, N_dual


def draw_normal(input_frame, fig, canvas):
    tk.Label(input_frame, text="Mean").pack()
    entry_mean = tk.Spinbox(input_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0"))
    entry_mean.pack()
    tk.Label(input_frame, text="SD").pack()
    entry_sd = tk.Spinbox(input_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1"))
    entry_sd.pack()

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
            tk.Spinbox(extra_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0")).pack()
        elif selection == "P(a<X<b)":
            tk.Label(extra_frame, text="a (lower)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="-0.25")).pack()
            tk.Label(extra_frame, text="b (upper)").pack()
            tk.Spinbox(extra_frame, from_=-1000, to=1000, textvariable=tk.StringVar(value="0.25")).pack()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)

    text_widget = tk.Text(input_frame, height=2, width=20)
    text_widget.pack(pady=15)

    def plot():
        mean = float(entry_mean.get())
        sd = float(entry_sd.get())
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        if selection == "Curve":
            N(ax, mean, sd)
        elif selection == "P(X≤x)":
            prob_X = N_left(ax, mean, sd, float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {float(spinboxes[0].get())}) = {prob_X:.4f}")
        elif selection == "P(X≥x)":
            prob_X = N_right(ax, mean, sd, float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {float(spinboxes[0].get())}) = {prob_X:.4f}")
        elif selection == "P(a≤X≤b)":
            prob_X = N_dual(ax, mean, sd, float(spinboxes[1].get()), float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob_X:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
