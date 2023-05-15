#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:09:17 2019

@author: gamma-dna
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import numpy.fft
import scipy.fftpack 

n = 1000
samp = []
ch1 = []
ch2 = []
ch3 = []
ch4 = []
df = pd.DataFrame(pd.read_csv('/home/gamma-dna/Desktop/Python_examples/OscilloscopeStream.csv'))
for i in xrange(len(df)):
    values = df.values[i][0].split(';')
    samp.append(int(values[0]))
    ch1.append(float(values[1]))
    ch2.append(float(values[2]))
    ch3.append(float(values[3]))
    ch4.append(float(values[4]))
y = list(ch1)
N = len(y)

x = np.linspace(1000, N*100, N)
yf = scipy.fftpack.fft(y) * 100
xf = np.linspace(0.0, 1/2.0, N/2)
fig, ax = plt.subplots()
ax.plot(xf * 100000, 2.0/N * np.abs(yf[:N//2]))
plt.show()