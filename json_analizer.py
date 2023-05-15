#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 12:15:13 2019

@author: gamma-dna
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib, json
import numpy as np
from pprint import pprint
matplotlib.style.use('ggplot')

time = []
voltage = []
voltage_json = []
cab = []

for i in xrange(4):
    n = str(i + 1)
    std = []
    for j in xrange(10):
        with open('/home/gamma-dna/Experiments/08.08.19/cabel_' + n + '_n' + str(j + 1) + '.json') as json_data:
            d = json.load(json_data)
            json_data.close()
        
        try:
            d = d[0][u'data']
        except KeyError:
            d = d[0][u'outputs'][0][u'data']
    
        for k in xrange(len(d)):
            voltage_json.append(d[k])
    
        mean = np.mean(voltage_json)
        var = np.var(voltage_json)
        std.append(np.std(voltage_json))
        amp = np.max(voltage_json) - np.min(voltage_json)
    print str(i+1) + ' ', std
    cab.append(np.mean(std))

print cab    