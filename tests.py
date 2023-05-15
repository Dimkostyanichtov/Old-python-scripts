#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 16:58:11 2019

@author: gamma-dna
"""
import visa, serial

rm = visa.ResourceManager()
instr_name = rm.list_resources()[0].encode('ascii')
ser = serial.Serial(instr_name.replace('ASRL', '').replace('::INSTR', '').strip(), timeout=1)

drain = 32595
drain_step = 1

for i in xrange(166):
    ser.write('SG1V' + str(drain) + '\r')
    print(ser.read(30))
    drain += drain_step

ser.close()