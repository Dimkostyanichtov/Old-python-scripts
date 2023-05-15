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

df = pd.DataFrame(pd.read_csv('/home/gamma-dna/Exper/DAC/27.05.2019/Battery2.csv')) #Считываем данные с файла
for i in xrange(len(df)):
    values = df.values[i][0].split(';')
    channel_1.append(float(values[1]))
    channel_2.append(float(values[2]))
    
h = 0.0001
    
for i in xrange(len(channel_1)): # Сигнал = переодический сигнал по первому каналу + шум по второму каналу
    signal.append(channel_1[i] + channel_2[i])

for j in xrange(len(signal)/2):
    Rxx = 0
    i = 1
    while i < (len(signal) - j):
        Rxx += signal[i]*signal[i+j]
        i += 1
    if j == 0:
        Rxx_max = Rxx
    corr_func.append(Rxx/Rxx_max)
    tau.append(j*h)

n = np.arange(len(signal))
fig, ax = plt.subplots() # Строим график
ax = plt.plot(n, signal, label=u'Измеренный сигнал с шумом')
ax = plt.plot(n, channel_1, label=u'Измеренный сигнал')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
fig, ax = plt.subplots() # Строим график
ax = plt.plot(tau, corr_func, label='Corellation func.')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()