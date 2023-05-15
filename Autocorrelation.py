#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 15:45:28 2019

@author: gamma-dna
"""
# Программа для расчёта автокорреляционной функции(АКФ)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib, json, datetime, os, io, sys
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
    load_name = int(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')

path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d'))

try:
    os.mkdir(path)
except OSError:
    path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d')) + '/'

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]
    
voltage_json = []

try:
    with open(load_name) as json_data:
        data_set = json.load(json_data)
        json_data.close()
    
    try:
        data = data_set[0][u'data']
    except KeyError:
        try:
            data = data_set[0][u'outputs'][0][u'data']
        except KeyError:
            try:
                data = data_set['median: ']
            except KeyError:
                data = data_set['x: ']
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
    
for i in xrange(len(data)):
    voltage_json.append(data[i])

corr_func = autocorr(voltage_json)

delay = np.arange(len(corr_func))
point_1 = 0
point_2 = 0
period = 0
point_3 = 0
point_4 = 0
period_2 = 0

for i in xrange(1, len(corr_func), 1):
    if corr_func[i] > corr_func[i-1] and corr_func[i] > corr_func[i+1]:
        point_1 = delay[i]
        for j in xrange(i+1, len(corr_func)):
            if corr_func[j] > corr_func[j - 1] and corr_func[j] > corr_func[j + 1]:
                point_2 = delay[j]
                break
            else: continue
        break
    else: continue

if point_2 > point_1:
    period = round((round(point_2, 8) - round(point_1, 5))/1000000, 8)
else:
    period = round((round(point_1, 8) - round(point_2, 5))/1000000, 8)
freq = round((1.0/period), 5)

corr_func = list(corr_func)
json_string = {'Autocorrelation: ': corr_func,
               'Frequency: ': freq,
               'Period: ': period
                       }
with io.open(path + 'Autocorrelation ' + save_name + '.json', 'w', encoding='utf8') as outfile:
    str_ = json.dumps(json_string,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii = True)
    outfile.write(unicode(str_))   

n = np.arange(len(voltage_json))
fig, ax = plt.subplots()
ax = plt.plot(n, voltage_json, label=u'Измеренный сигнал')
plt.xlabel('Points')
plt.ylabel('Signal')
plt.legend(loc='best')
fig, ax = plt.subplots()
ax = plt.plot(delay, corr_func, label='Period is ' + str(period) + ' sec.\n' + u'Frequency is ' + str(freq) + ' Hz')
plt.xlabel('Delay')
plt.ylabel('Autocorrelation func.')
plt.legend(loc='best')
plt.show()
sys.exit(0)