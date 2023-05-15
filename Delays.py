#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 18:21:48 2019

@author: gamma-dna
"""
# Программа для подсчёта задержек при заданном пороге для растворов

import yaml, datetime, os, json, io, sys
import pandas as pd

# Функция для расчёта задержек
def delay(load_name, threshhold):
    
    voltage_json = [] # инициализация массива для сигнала, массив один, так как данные есть экспорт по одному из каналов TiePie
# в программе MultiChannel

    # Считывание данных из файла json
    try:
        with open(load_name) as json_data: # в кавычках прописан путь к файлу
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

    # Записываем сигнал        
    for k in xrange(len(data)):
        voltage_json.append(data[k])
    
    delays = [] # массив для задержек 
    zero_count = 0 # задержка
    step = 1 # шаг по измерениям
    i=0

    while i <len(voltage_json):
    #for i in range(len(voltage_json), step): # начинаем не с 0 а с n (например, 10), т.к. около нуля есть флуктуации измерений
        if float(voltage_json[i]) > threshhold and float(voltage_json[i-1]) < threshhold and zero_count != 0: # если измерение больше, чем порог, и задержка не равна 0, то
            delays.append(zero_count) # записываем задержку в массив и
            zero_count = jump # обнуляем задержку, при этом
            step = jump
        elif float(voltage_json[i]) > threshhold and float(voltage_json[i-1]) > threshhold:
            zero_count = 0
            step = 1
            #continue
        elif float(voltage_json[i]) > threshhold and float(voltage_json[i-1]) < threshhold and zero_count == 0: # если значение больше порога, и задержка равна 0, то
            zero_count += 1 # инкрементируем заержку и 
            step = 1 # задаём шаг 1
        elif float(voltage_json[i]) <= threshhold and float(voltage_json[i-1]) < threshhold: # если измерение меньше порога, то
            zero_count += 1 # инкрементируем задержку
            step = 1 # меняем шаг на 1
        elif float(voltage_json[i]) <= threshhold and float(voltage_json[i-1]) > threshhold:
            zero_count = 1
            step = 1 # изменияем шаг по массиву измерений для "перепрыгивания" колебаний переходного процесса
        elif i == len(voltage_json): # если порог так и не был превышен, то
            delays.append(zero_count) # записываем полную задержку
        i+=step
    
    return(delays)

print(u'Введите название исходного файла для раствора "min T" (полный путь):')
try:
    T_load_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите порог для раствора "min T":')
try:
    T_threshhold = float(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1) # порог, В
print('\n')
print(u'Введите название исходного файла для раствора "min A" (полный путь):')
try:
    A_load_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите порог для раствора "min A":')
try:
    A_threshhold = float(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1) # порог, В
print('\n')
print(u'Введите название исходного файла для раствора "min C" (полный путь):')
try:
    C_load_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите порог для раствора "min C":')
try:
    C_threshhold = float(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1) # порог, В
print('\n')
print(u'Введите название исходного файла для раствора "min G" (полный путь):')
try:
    G_load_name = raw_input()
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1)
print('\n')
print(u'Введите порог для раствора "min G":')
try:
    G_threshhold = float(input())
except NameError:
    print(u'Введены неверные данные!')
    sys.exit(1) # порог, В
print('\n')
print(u'Введите название файла для сохранения результатов:')
save_name = raw_input()
print(u'Введите "задержку" после сигнала (шт. измерений):') # количество значений, через которое "перепрыгнет" программа при превышении порога
jump = int(input())
print('\n')

path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d'))

try:
    os.mkdir(path)
except OSError:
    path = '/home/gamma-dna/Results of programs/' + str(datetime.datetime.today().strftime('%Y.%m.%d')) + '/'


T_delays = delay(T_load_name, T_threshhold)
A_delays = delay(A_load_name, A_threshhold)
C_delays = delay(C_load_name, C_threshhold)
G_delays = delay(G_load_name, G_threshhold)


# Форматируем данные для записи в yaml
to_yaml = {
           'dnaSize': 177,
           'primer': 'GTACACTACATGTCCATAGCAGGCTTG',
           'primerOffset': 15,
           'stages': [{'reducedNucleotide': "T", 'delays': T_delays},
                      {'reducedNucleotide': "A", 'delays': A_delays},
                      {'reducedNucleotide': "C", 'delays': C_delays},
                      {'reducedNucleotide': "G", 'delays': G_delays}]
           }

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True

# записываем yaml
data = "---\n{}".format(yaml.dump(to_yaml, Dumper=NoAliasDumper, default_flow_style=False))

with io.open(path + 'Delays ' + save_name + '.yaml', 'w') as outfile:
    outfile.write(unicode(data))
sys.exit(0)