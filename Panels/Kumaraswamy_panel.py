import tkinter as tk
from tkinter import ttk

from Distributions.Kumaraswamy_dist import Kuma, Kuma_left, Kuma_right, Kuma_between


def draw_kumaraswamy(input_frame, fig, canvas):
    tk.Label(input_frame, text="a").pack()
    entry_a = tk.Spinbox(input_frame, from_=0.01, to=1000, increment=0.1, textvariable=tk.StringVar(value="10"))
    entry_a.pack()
    tk.Label(input_frame, text="b").pack()
    entry_b = tk.Spinbox(input_frame, from_=0.01, to=1000, increment=0.1, textvariable=tk.StringVar(value="15"))
    entry_b.pack()

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
            tk.Spinbox(extra_frame, from_=0, to=1, increment=0.01, textvariable=tk.StringVar(value="0.5")).pack()
        elif selection == "P(a≤X≤b)":
            tk.Label(extra_frame, text="lower").pack()
            tk.Spinbox(extra_frame, from_=0, to=1, increment=0.01, textvariable=tk.StringVar(value="0.3")).pack()
            tk.Label(extra_frame, text="upper").pack()
            tk.Spinbox(extra_frame, from_=0, to=1, increment=0.01, textvariable=tk.StringVar(value="0.8")).pack()
        plot()

    combo_box.bind("<<ComboboxSelected>>", update_extra_inputs)

    text_widget = tk.Text(input_frame, height=2, width=20)
    text_widget.pack(pady=15)

    def plot():
        a = float(entry_a.get())
        b = float(entry_b.get())
        fig.clear()
        ax = fig.add_subplot(111)
        selection = combo_box.get()
        spinboxes = [w for w in extra_frame.winfo_children() if isinstance(w, tk.Spinbox)]
        if selection == "Curve":
            Kuma(ax, a=a, b=b)
        elif selection == "P(X≤x)":
            prob = Kuma_left(ax, a=a, b=b, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≤ {float(spinboxes[0].get())}) = {prob:.4f}")
        elif selection == "P(X≥x)":
            prob = Kuma_right(ax, a=a, b=b, param=float(spinboxes[0].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P(X ≥ {float(spinboxes[0].get())}) = {prob:.4f}")
        elif selection == "P(a≤X≤b)":
            prob = Kuma_between(ax, a=a, b=b, param1=float(spinboxes[0].get()), param2=float(spinboxes[1].get()))
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, f"P({float(spinboxes[0].get())} ≤ X ≤ {float(spinboxes[1].get())}) = {prob:.4f}")
        canvas.draw()

    tk.Button(input_frame, text="Plot", command=plot).pack(pady=5)
    plot()
