# -*- coding: utf-8 -*-
"""
Created on Sun May 17 08:29:31 2026

@author: snaph
"""

import tkinter as tk
from Distributions.Normal_dist import N, N_left, N_right, N_dual

root = tk.Tk()
root.title("Distribution Calculator")

btn = tk.Button(root, text="Calculate", command=lambda: print("Calculate clicked"))
btn.pack(pady=20)

N()

root.mainloop()
