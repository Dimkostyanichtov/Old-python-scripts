#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:13:45 2019

@author: gamma-dna
"""

import serial, time

ser = serial.Serial('/dev/ttyPUMP', timeout=1)
ser.write('/1ZR\r'.encode())
time.sleep(2)
