#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:31:25 2019

@author: gamma-dna
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, json
import numpy as np
from pprint import pprint
matplotlib.style.use('ggplot')

voltage_csv = []
    
df1 = pd.DataFrame(pd.read_csv('/home/gamma-dna/Programs for signals/OscilloscopeStream.csv'))

for i in xrange(10, len(df1)):
    try:
        if df1.values[i][0].split(';')[1] != 'nan':
            voltage_csv.append(float(df1.values[i][0].split(';')[1]))
    except ValueError:
        continue

var = np.var(voltage_csv)
mean = np.mean(voltage_csv)
print var, mean