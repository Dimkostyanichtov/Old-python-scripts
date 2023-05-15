#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:35:12 2019

@author: gamma-dna
"""

filename = '/home/gamma-dna/Experiments/int8_01_041.bin'

with open(filename, "rb") as bin_file:
    m = bin_file.read(50)
    print(m)