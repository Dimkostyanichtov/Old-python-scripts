#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 12:02:33 2019

@author: gamma-dna
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.style.use('ggplot')

samp = []
ch1 = []
ch2 = []
ch3 = []

df1 = pd.DataFrame(pd.read_csv('/home/gamma-dna/Desktop/Python_examples/OscilloscopeStream.csv'))
for i in xrange(len(df1)):
    values = df1.values[i][0].split(';')
    samp.append(int(values[0]))
    ch1.append(float(values[1]))
    ch2.append(float(values[2]))
    ch3.append(float(values[3]))

if max(ch1) > 0 and min(ch1) >= 0 or max(ch1) >= 0 and min(ch1) < 0:
    amplitude1 = max(ch1) - min(ch1)
elif max(ch1) <= 0 and min(ch1) < 0:
    amplitude1 = max(ch1) + abs(min(ch1))
if max(ch2) > 0 and min(ch2) >= 0 or max(ch2) >= 0 and min(ch2) < 0:
    amplitude2 = max(ch2) - min(ch2)
elif max(ch2) <= 0 and min(ch2) < 0:
    amplitude2 = max(ch2) + abs(min(ch2))
if max(ch3) > 0 and min(ch3) >= 0 or max(ch3) >= 0 and min(ch3) < 0:
    amplitude3 = max(ch3) - min(ch3)
elif max(ch3) <= 0 and min(ch3) < 0:
    amplitude3 = max(ch3) + abs(min(ch3))
mean1 = round(np.mean(ch1), 6)*1000000
mean2 = round(np.mean(ch2), 6)*1000000
mean3 = round(np.mean(ch3), 6)*1000000
var1 = np.std(ch1)*1000000
var2 = np.std(ch2)*1000000
var3 = np.std(ch3)*1000000
plt.plot(samp, ch1, label= 'Ch1:' + '\n' + 'Offset = ' + str(mean1) + '\n' + 'Otklonenie = ' + str(var1) + '\n' + ' Amplitude = ' + str(amplitude1*1000000))
plt.xlabel('Sample')
plt.ylabel('Volts')
plt.legend(loc='best')
plt.plot(samp, ch2, label= 'Ch2:' + '\n' + 'Offset = ' + str(mean2) + '\n' + 'Otklonenie = ' + str(var2) + '\n' + ' Amplitude = ' + str(amplitude2*1000000))
plt.xlabel('Sample')
plt.ylabel('Volts')
plt.legend(loc='best')
plt.plot(samp, ch3, label= 'Ch3:' + '\n' + 'Offset = ' + str(mean3) + '\n' + 'Otklonenie = ' + str(var3) + '\n' + ' Amplitude = ' + str(amplitude3*1000000))
plt.xlabel('Sample')
plt.ylabel('Volts')
plt.legend(loc='best')
plt.show()