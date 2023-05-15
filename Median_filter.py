#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 16:04:24 2019

@author: gamma-dna
"""
# Программа медианного фильтра данных

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, json, io, os, datetime, sys
matplotlib.style.use('ggplot')

# Функция для медианной фильтрации
def median_filter(data, window, samp_freq):
    
    h = 1.0/samp_freq # Наг по времени
    t_n = 0.0
    t = []
    median = []

    for i in xrange(len(data) - window):
        mean = np.mean(data[i:i+window]) 
        median.append(data[i] - mean) # Медианная филтьрация
        t_n += h
        t.append(t_n)
        
    return median, t

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
print(u'Введите ширину окна:')
try:
    window = int(input())
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
    with open(load_name) as json_data: # В кавычках задаётся путь к файлу
        data_set = json.load(json_data)
        json_data.close()
    
    try:
        data = data_set['x: ']
    except TypeError:
        try:
            data = data_set[0][u'data']
        except KeyError:
            data = data_set[0][u'outputs'][0][u'data']
        except KeyError:
            print(u'Указан неверный формат файла!')
            sys.exit(1)
except ValueError:
    
    data = []
    data_set = pd.DataFrame(pd.read_csv(load_name))
    
    for i in xrange(10, len(data_set)):
        try:
            if data_set.values[i][0].split(';')[1] != 'nan':
                data.append(float(data_set.values[i][0].split(';')[1]))
        except ValueError:
            continue

median, t = median_filter(data, window, samp_freq)
    
json_string = {
               'median: ': median,
               't: ': t
                       }

with io.open(path + 'Median filter ' + save_name + '.json', 'w') as outfile:
    str_ = json.dumps(json_string,
                      indent=4, sort_keys=False,
                      separators=(',', ': '))
    outfile.write(unicode(str_))   
   
# Задаём диапазон значений графика
n1 = np.arange(len(data))
# Строим график
fig, ax = plt.subplots() # Строим график
ax = plt.plot(t, median, label=u'Медианный фильтр')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
fig, ax = plt.subplots() # Строим график
ax = plt.plot(n1, data, label=u'Исходные данные')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
sys.exit(0)