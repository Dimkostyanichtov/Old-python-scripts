#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 14:40:25 2019

@author: gamma-dna
"""

import serial
import time, visa

rm = visa.ResourceManager()
print(rm.list_resources())
ser = serial.Serial('/dev/ttyUSB0', timeout=1)
ser.write(b'A\xFF\xFF')

time.sleep(1)

ser.write(b'B\x00\x00')
print(ser.read(2))
ser.close()