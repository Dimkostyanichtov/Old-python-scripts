#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 09:53:23 2018

@author: gamma-dna
"""

import visa
import time
import matplotlib.pyplot as plt


rm = visa.ResourceManager()
print(rm.list_resources())
instr = rm.open_resource('ASRL/dev/ttyUSB1::INSTR')
instr.write('/1ZR\r')
instr.write('*TRG')
print(instr.query('*IDN?'))
time.sleep(0.05)
instr.close()
