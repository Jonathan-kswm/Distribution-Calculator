#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 02:22:26 2026

@author: jonathanhoward
"""

import pypdf as pdf

f = open("normal.pdf", "rb")

pdf_reader = pdf.PdfFileReader(f)

pdf_reader.getPage(0).extractText()
