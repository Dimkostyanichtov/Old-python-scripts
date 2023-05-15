#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:26:13 2019

@author: gamma-dna
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

n = int(input())
sr = []
samp = []
ch1 = []

df = pd.DataFrame(pd.read_csv('/home/gamma-dna/Desktop/Python_examples/OscilloscopeStream.csv'))
for i in xrange(len(df)):
    values = df.values[i][0].split(';')
    samp.append(int(values[0]))
    ch1.append(float(values[1]))

for i in xrange(len(ch1) - n):
    sr.append(np.mean(ch1[i:i+n]))
for i in xrange(n):
    sr.append(sr[(len(sr)-n+i)])

t = np.arange(len(sr))    
fig, ax = plt.subplots()
ax = plt.plot(t, sr, label=u'Плавающее окно', color='blue')
plt.legend(loc='best')
plt.xlabel(u'Время')
plt.ylabel(u'Сигнал')
plt.show()
fig, ax = plt.subplots()
ax = plt.plot(t, ch1, label=u'Исходные данные', color='blue')
plt.legend(loc='best')
plt.xlabel(u'Время')
plt.ylabel(u'Сигнал')
plt.show()