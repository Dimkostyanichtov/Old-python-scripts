# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import visa
import matplotlib.pyplot as plt
import numpy as np
#import DevMeasMod

rm = visa.ResourceManager()
inname = rm.list_resources()[0].encode('ascii')
instr = rm.open_resource(inname)

dispdat1 = list(instr.query('CHAN1:DATA?').split(','))
for i in range(len(dispdat1)):
    dispdat1[i] = float(dispdat1[i])
dispdat2 = list(instr.query('CHAN2:DATA?').split(','))
for i in range(len(dispdat2)):
    dispdat2[i] = (float(dispdat2[i]))/100   

#instr.write('GEN:VOLT:OFFS 2.0')

#print(dispdat1, 'ASSSFAF', dispdat2)   
fig, ax = plt.subplots()
ax.plot(dispdat1, dispdat2, color = 'red', label = u'Осциллограф')
ax.set_xlabel(u'Напряжение')
ax.set_ylabel(u'Ток')
ax.legend()
plt.show()
