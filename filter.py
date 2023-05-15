#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 16:07:40 2019

@author: gamma-dna
"""

import visa

rm = visa.ResourceManager()
print(rm.list_resources())
instr = rm.open_resource('ASRL/dev/ttyUSB0::INSTR')
#instr.write('/1ZR\r')
instr.write('/1V300M1000O4M1000A2000M1000O5A0R\r')