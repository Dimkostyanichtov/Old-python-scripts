#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 10:22:23 2019

@author: gamma-dna
"""
# Программа для реализации стохастического резонанса методом Рунге-Кутты

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, sys
import json, datetime, os, io
matplotlib.style.use('ggplot')

print(u'Введите название исходного файла (полный путь):')
try:
    load_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите название файла для сохранения результатов:')
try:
    save_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите частоту сэмплирования данных в исходном файле:')
try:
    samp_freq = int(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите коэффициент усиления (по умолчанию 1):')
try:
    ampl = float(input())
except SyntaxError:
    ampl = 1
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите коэффициент смещения (по умолчанию 0):')
try:
    offset = float(input())
except SyntaxError:
    offset = 0
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
    
path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d'))

try:
    os.mkdir(path)
except OSError:
    path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d')) + '/'

x = [[0.0, 0.0],[0.0, 0.0]] # массив, содержащий переменные модельного уравнения и их первые производные
t = 0.0 # текущий отсчёт по времени
h = 1.0/samp_freq # шаг по времени, вычисляется как 1/частоту сэмплирования

# реализация метода       
def Runge_Kutt(signal, x, t, h):
        
    x_n, t_n = [], []
    
    for i in xrange(len(signal) - 1):
        
        xk = x[1][0]
        
        x[1][1] = x[1][0] - x[1][0]**3 + signal[i]
        k1 = x[1][1] * h
        x[1][0] = xk + k1*0.5
            
        t = t + 0.5*h
        x[1][1] = x[1][0] - x[1][0]**3 + signal[i]
        k2 = x[1][1] * h
        x[1][0] = xk + k2*0.5
            
        x[1][1] = x[1][0] - x[1][0]**3 + signal[i]
        k3 = x[1][1] * h
        x[1][0] = xk + k3
            
        t = t + 0.5*h
        x[1][1] = x[1][0] - x[1][0]**3 + signal[i]
        k4 = x[1][1] * h
        x[1][0] = (xk + (k1 + 2*k2 + 2*k3 + k4)/6)
        x_n.append(x[1][0])
        t_n.append(t)
        
    return x_n, t_n

signal = []

# Считывание с файла json
try:
    with open(load_name) as json_data:
        data_set = json.load(json_data)
        json_data.close()
    
    try:
        data = data_set['median: ']
    except TypeError:
        try:
            data = data_set[0][u'data']
        except KeyError:
            data = data_set[0][u'outputs'][0][u'data']
except ValueError:
    
    data = []
    data_set = pd.DataFrame(pd.read_csv(load_name))
    
    for i in xrange(10, len(data_set)):
        try:
            if data_set.values[i][0].split(';')[1] != 'nan':
                data.append(float(data_set.values[i][0].split(';')[1]))
        except ValueError:
            continue

# Запись сигнала
for i in xrange(len(data)):
    signal.append((data[i]*ampl) + offset) # задание шумового смещения

x_n, t_n = Runge_Kutt(signal, x, t, h) # применяем метод

json_string = {'x: ': x_n,
               't: ': t_n,
                       }
with io.open(path + 'Runge-Kutt ' + save_name + '.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(json_string,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii=True)
    outfile.write(unicode(str_))   

# Задаём диапазон значений графика
n = np.arange(len(signal))
# Строим график
fig, ax = plt.subplots() # Строим график
ax = plt.plot(n, signal, label=u'Измеренный сигнал')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
fig, ax = plt.subplots() # Строим график
ax = plt.plot(t_n, x_n, label=u'Метод Рунге-Кутты')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
sys.exit(0)