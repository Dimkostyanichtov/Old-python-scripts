#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 13:15:59 2018

@author: gamma-dna
"""

import sys, visa
import DevMeasMod as dmm
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication


app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
data = dmm.DataInput()
app.exec_()

if data.ex_event == True:
    instr1 = dmm.Device()
    instr2 = dmm.Device()
    instr3 = dmm.Device()
    instr4 = dmm.Device()

    instr1.initdev(data.filename)
    instr2.initdev(data.filename)
    instr4.initdev(data.filename)
    
    instr1.instr_connect('Pump')
    instr2.instr_connect('Generator')
    instr3.instr_connect('Microscope')
    instr4.instr_connect('Oscilophone')

    instr1.pump("/1V300M1000O5M1000A3000M1000A0R\r", 20)
    instr2.gen_output('1', 'SIN', '2', '200', '1', '40')
    instr2.gen_output('2', 'SQU', '2', '400', '0.5', '40')
    instr4.oscil_write(data.savename, data.myname, data.expname, data.expnumb, 10)
    instr2.gen_reset('1', 12)
    instr2.gen_reset('2', 0)
    instr3.micro()
    instr1.instr_disc()
    instr2.instr_disc()
    instr4.instr_disc()

else:
    sys.exit()
    
print('Готово')