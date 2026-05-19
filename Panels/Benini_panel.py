import tkinter as tk
from tkinter import ttk

from Distributions.Benini_dist import (
    Benini10, Benini10_left, Benini10_right, Benini10_between,
    Benini_e, Benini_e_left, Benini_e_right, Benini_e_between,
)


def draw_benini(input_frame, fig, canvas):
    log_base = tk.StringVar(value="e")
    check_e_var = tk.BooleanVar(value=True)
    check_10_var = tk.BooleanVar(value=False)

    def select_e():
        log_base.set("e")
        check_e_var.set(True)
        check_10_var.set(False)
        plot()

    def select_10():
        log_base.set("10")
        check_e_var.set(False)
        check_10_var.set(True)
        plot()

    tk.Label(input_frame, text="Log Base").pack()
    tk.Checkbutton(input_frame, text="ln (base e)", variable=check_e_var, command=select_e).pack()
    tk.Checkbutton(input_frame, text="log (base 10)", variable=check_10_var, command=select_10).pack()

    tk.Label(input_frame, text="α (alpha)").pack()
    entry_a = tk.Spinbox(input_frame, from_=0, to=1000, increment=0.1, textvariable=tk.StringVar(value="4"))
    entry_a.pack()
    tk.Label(input_frame, text="β (beta)").pack()
    entry_b = tk.Spinbox(input_frame, from_=0, to=1000, increment=0.1, textvariable=tk.StringVar(value="4"))
    entry_b.pack()
    tk.Label(input_frame, text="σ (sigma)").pack()
    entry_s = tk.Spinbox(input_frame, from_=0.01, to=1000, increment=0.1, textvariable=tk.StringVar(value="4"))
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
            tk.Spinbox(extra_frame, from_=0, to=1000, increment=0.1, textvariable=tk.StringVar(value="5")).pack()
        elif selection == "P(a≤X≤b)":
            tk.Label(extra_frame, text="a (lower)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, increment=0.1, textvariable=tk.StringVar(value="5")).pack()
            tk.Label(extra_frame, text="b (upper)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, increment=0.1, textvariable=tk.StringVar(value="7")).pack()
        plot()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)

    text_widget = tk.Text(input_frame, height=6, width=20)
    text_widget.pack(pady=15)

    def plot():
        a = float(entry_a.get())
        b = float(entry_b.get())
        s = float(entry_s.get())
        base = log_base.get()
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]

        if base == "e":
            curve_fn, left_fn, right_fn, between_fn = Benini_e, Benini_e_left, Benini_e_right, Benini_e_between
        else:
            curve_fn, left_fn, right_fn, between_fn = Benini10, Benini10_left, Benini10_right, Benini10_between

        if selection == "Curve":
            curve_fn(ax, a=a, b=b, s=s)
        elif selection == "P(X≤x)":
            prob = left_fn(ax, a=a, b=b, s=s, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {float(spinboxes[0].get())}) = {prob:.4f} \n \nPlease Note that the Benini distribution is only defined for P(X≤σ)  ")
        elif selection == "P(X≥x)":
            prob = right_fn(ax, a=a, b=b, s=s, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {float(spinboxes[0].get())}) = {prob:.4f}")
        elif selection == "P(a≤X≤b)":
            prob = between_fn(ax, a=a, b=b, s=s, param1=float(spinboxes[0].get()), param2=float(spinboxes[1].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
