#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:19:38 2019

@author: gamma-dna
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

corr_func = []
channel_1 = []
channel_2 = []
signal = []
tau = []

df = pd.DataFrame(pd.read_csv('/home/gamma-dna/Desktop/Python_examples/OscilloscopeStream.csv'))
for i in xrange(len(df)):
    values = df.values[i][0].split(';')
    channel_1.append(float(values[1]))
    channel_2.append(float(values[2]))
    
h = 0.0001
    
for i in xrange(len(channel_1)):
    signal.append(channel_1[i] + channel_2[i])

for j in xrange(len(signal)/2):
    Rxx = 0.0
    i = 1
    while i < (len(signal) - j):
        Rxx += signal[i]*signal[i+j]
        i += 1
    if j == 0:
        Rxx_max = Rxx
    corr_func.append(Rxx/Rxx_max)
    tau.append(j*h)

period_1 = 0
period_2 = 0
period = 0
for i in xrange(1, len(corr_func) - 1):
    if corr_func[i] > corr_func[i-1] and corr_func[i] > corr_func[i+1]:
        period_1 = tau[i]
        for j in xrange(i+1, len(corr_func) - 1 - i):
            if corr_func[j] > corr_func[j - 1] and corr_func[j] > corr_func[j + 1]:
                period_2 = tau[j]
                break
            else: continue
        break
    else: continue
period = round((period_2 - period_1)/100, 12)
freq = int(round(1/period))
    
n = np.arange(len(signal))
fig, ax = plt.subplots()
ax = plt.plot(n, signal, label=u'Измеренный сигнал с шумом')
ax = plt.plot(n, channel_1, label=u'Измеренный сигнал')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
fig, ax = plt.subplots()
ax = plt.plot(tau, corr_func, label='Period = ' + str(period) + ' sec.\n' + 'Frequency = ' + str(freq) + ' Hz')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()