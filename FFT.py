#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 15:38:47 2019

@author: gamma-dna
"""

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd

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
v=list(ch1)
T=np.pi;z=T/16; m=[k*z for k in np.arange(0,len(v),1)];arg=[];q=[]#  16 отсчётов на период в пи
F=np.fft.rfft(v, n=None, axis=-1) # прямое быстрое преобразование Фурье в частотную область
a = len(F)
A=[((F[i].real)**2+(F[i].imag)**2)**0.5 for i in np.arange(0, a, 1)]#модуль амплитуды
for i in np.arange(0,a,1):# определение фазы
         if F[i].imag!=0:
                  t=(-np.tanh((F[i].real)/(F[i].imag)))
                  arg.append(t)                  
         else:
                arg.append(np.pi/2)
plt.figure()
plt.title(u"Спектральный анализ с использованием  прямого БПФ ")
plt.plot(np.arange(0, a, 1),arg,label=u'Фаза')
plt.plot(np.arange(0, a, 1),A,label=u'Амплитуда')
plt.xlabel(u"Частота")
plt.ylabel(u"Фаза,Амплитуда")
print(A.index(max(A)))
plt.legend(loc='best')
plt.grid(True)
for i in np.arange(0, a, 1):
         if i<=7:
                  q.append(F[i])
         else:
                  q.append(0)
h=np.fft.irfft(q, n=None, axis=-1)# обратное быстрое преобразование Фурье во временную область
plt.figure()
plt.title(u"Спектральный синтез с использованием  обратного БПФ ")
plt.plot(m, v,label=u'Исходная функция')
plt.plot(m, h,label=u'Синтезированная функция')
plt.xlabel(u"Время")
plt.ylabel(u"Амплитуда")
plt.legend(loc='best')
plt.grid(True)          
plt.show()