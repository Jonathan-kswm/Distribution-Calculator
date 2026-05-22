import tkinter as tk
from tkinter import ttk

from Distributions.Chi_squared_dist import chi_squared, chi_squared_left, chi_squared_right, chi_squared_between


def draw_chi_squared(input_frame, fig, canvas):
    tk.Label(input_frame, text="Degrees of freedom (k)").pack()
    entry_df = tk.Spinbox(input_frame, from_=1, to=1000, textvariable=tk.StringVar(value="3"))
    entry_df.pack()

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
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1")).pack()
        elif selection == "P(a≤X≤b)":
            tk.Label(extra_frame, text="a (lower)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="1")).pack()
            tk.Label(extra_frame, text="b (upper)").pack()
            tk.Spinbox(extra_frame, from_=0, to=1000, textvariable=tk.StringVar(value="4")).pack()
        plot()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)

    text_widget = tk.Text(input_frame, height=2, width=20)
    text_widget.pack(pady=15)

    def plot():
        df = float(entry_df.get())
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        if selection == "Curve":
            chi_squared(ax, df=df)
        elif selection == "P(X≤x)":
            prob_X = chi_squared_left(ax, df=df, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {float(spinboxes[0].get())}) = {prob_X:.4f}")
        elif selection == "P(X≥x)":
            prob_X = chi_squared_right(ax, df=df, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {float(spinboxes[0].get())}) = {prob_X:.4f}")
        elif selection == "P(a≤X≤b)":
            prob_X = chi_squared_between(ax, df=df, param1=float(spinboxes[0].get()), param2=float(spinboxes[1].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob_X:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
