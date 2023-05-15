#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 14:01:25 2019

@author: gamma-dna
"""
import time, visa

rm = visa.ResourceManager()
print(rm.list_resources())
instr = rm.open_resource('ASRL/dev/ttyACM0::INSTR')

dispdat_1 = []
dispdat_2 = []
exposed_time = 0
dispdat_1_list = []
dispdat_2_list = []
        
instr.write('CHAN2:STAT ON')
time.sleep(0.5)
instr.write('CHAN1:STAT ON')
time.sleep(0.05)
start_time = time.time()
while 10 > exposed_time:
    exposed_time = time.time() - start_time
    instr.write('CHAN1:STAT ON')
    dispdat_1.append(instr.query('CHAN1:DATA?').split(','))
    instr.write('CHAN2:STAT ON')
    dispdat_2.append(instr.query('CHAN2:DATA?').split(','))
    continue
for i in xrange(len(dispdat_1)):
    for j in range(len(dispdat_1[i])):
        dispdat_1[i][j] = round(float(dispdat_1[i][j]), 6)
        #dispdat_2[i][j] = round(float(dispdat_2[i][j]), 6)
        dispdat_1_list.append(dispdat_1[i][j])
        #dispdat_2_list.append(dispdat_2[i][j])