#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 15:06:34 2019

@author: gamma-dna
"""
# Программа для фильтрации гармонических помех адаптивным фильтром
# На больших данных эта программа работает медленно, лучше обрабатывать файлы не длиннее нескольких тысяч значений

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, json, io, os, datetime, sys
matplotlib.style.use('ggplot')

# channel_1 и channel_2 - списки для записи данных по соответствующим каналам. Для записи по каналам 3 и 4 добавить соответствующие списки.

channel_1 = []
channel_2 = []
signal = []

def smart_filter(signal, samp_freq, h, m):
    
    rpt = 3 # Число проходов фильтра

    b = np.zeros(len(signal)) # начальный массив из нулей для настраиваемых коэффициентов b
    x = np.zeros(len(signal)) # начальный массив из нулей для помехи

    for i in xrange(rpt): # проход по сигналу
    
        t = []
        s = []
        
        for j in xrange(len(signal)): # непосредственно настройка

            y = 0.0
            for k in xrange(1, len(signal)): x[k] = x[k-1] # сдвиг сигнала помехи по рабочему массиву
            x[1] = signal[j] # загрузка сигнала помехи в рабочий массив
            for k in xrange(len(signal)): y += x[k]*b[k] # вычисляем сумму по всем весовым коэффициентам для сигнала помехи
            # защита от неустойчивости - может возникнуть при больших m:
            if y > 1.0:
                y = 1.0
            elif y < (-1.0):
                y = (-1.0)
            s.append(signal[j] - y) # вычитаем вычисленный отсчёт сигнала помехи из исходного сигнала
            # защита от неустойчивости
            if s[j] > 1.0:
                s[j] = 1.0
            elif s[j] < (-1.0):
                s[j] = (-1.0)
            # вычисляем время, соответствующее текущему отсчёту исходного сигнала:
            if j == 0:
                t.append(h)
            else:
                t.append(t[j - 1] + h)
            # вычисляем новые значения весовых коэффициентов b:
            c = 2*m*s[j]
            for k in xrange(len(signal)):
                b[k] += x[k]*c
        
    return b, t, s

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

path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d'))

try:
    os.mkdir(path)
except OSError:
    path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d')) + '/'

# Этот блок нужен для открытия json формата. Ниже есть закомментированный блок для работы с csv 
try:
    with open('/home/gamma-dna/Experiments/12.08.2019/noise.json') as json_data: # В кавычках задаётся путь к файлу
        data_set = json.load(json_data)
        json_data.close()

    try:
        data = data_set[0][u'data']
    except KeyError:
        data = data_set[0][u'outputs'][0][u'data']
        
    for i in xrange(len(data)):
        signal.append(data[i])
except ValueError:
    
    data = []
    data_set = pd.DataFrame(pd.read_csv(load_name))
    
    for i in xrange(10, len(data_set)):
        try:
            if data_set.values[i][0].split(';')[1] != 'nan':
                data.append(float(data_set.values[i][0].split(';')[1]))
        except ValueError:
            continue

# Настраиваемые коэффициенты:    
m = 0.0008 # константа, задающая скорость адаптации фильтра
h = 1.0/samp_freq # шаг дискретизации по времени, если не выходит результат, то можно поменять его порядок в большую или меньшую стороны,
# изначальное значение равно 1/частоту семплирования данных в файле

b, t, s = smart_filter(signal, samp_freq, h, m)

b = list(b)
json_string = {
               'h: ': h,
               'm: ': m,
               'data: ': b
                       }
with io.open(path + 'Smart filter ' + save_name + '.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(json_string,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii = True)
    outfile.write(unicode(str_))   
           
# Построение графика
n = np.arange(len(signal)) # Задаём диапазон значений графиков
fig, ax = plt.subplots() # Строим график
ax = plt.plot(n, signal, label=u'Измеренный сигнал')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
fig, ax = plt.subplots() # Строим график
ax = plt.plot(t, s, label=u'Восстановленный сиsгнал')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
sys.exit(0)