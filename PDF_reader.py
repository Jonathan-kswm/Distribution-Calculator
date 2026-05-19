#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 02:22:26 2026

@author: jonathanhoward
"""

import tkinter as tk
import fitz


def show_pdf(master, pdf_path, width=600, height=800):
    frame = tk.Frame(master)
    canvas = tk.Canvas(frame, width=width, height=height, bg="white",
                       highlightthickness=0)
    vbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vbar.set)
    vbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    images = []
    y = 0
    max_w = 0
    doc = fitz.open(pdf_path)
    for page in doc:
        pix = page.get_pixmap()
        if pix.alpha:
            pix = fitz.Pixmap(pix, 0)
        img = tk.PhotoImage(master=master, data=pix.tobytes("ppm"))
        images.append(img)
        canvas.create_image(0, y, image=img, anchor="nw")
        y += pix.height
        max_w = max(max_w, pix.width)
    doc.close()

    canvas.configure(scrollregion=(0, 0, max_w, y))
    # Keep image refs alive for the lifetime of the frame.
    frame.images = images

    canvas.bind("<Enter>", lambda _e: canvas.bind_all(
        "<MouseWheel>",
        lambda e: canvas.yview_scroll(int(-e.delta / 120), "units")))
    canvas.bind("<Leave>", lambda _e: canvas.unbind_all("<MouseWheel>"))

    return frame

#def print_pdf():
    


if __name__ == "__main__":
    root = tk.Tk()
    root.title("PDF Reader")
    show_pdf(root, "pdfs/normal.pdf").pack(fill="both", expand=True)
    root.mainloop()
