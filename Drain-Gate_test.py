#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 14:43:46 2019

@author: gamma-dna
"""
import time, os, sys, visa, libtiepie, serial

delay = 1
drain = 45000
drain_step = 300
gate = 40000
gate_step = 200
n_steps = 20
n = 1
voltage = 0

libtiepie.device_list.update()
rm = visa.ResourceManager()
print(rm.list_resources())
instr_name = rm.list_resources()[0].encode('ascii')
ser = serial.Serial(instr_name.replace('ASRL', '').replace('::INSTR', '').strip(), timeout=1)

scp = None
for item in libtiepie.device_list:
    if item.can_open(libtiepie.DEVICETYPE_OSCILLOSCOPE):
        scp = item.open_oscilloscope()
        if scp.measure_modes & libtiepie.MM_STREAM:
            break
        else:
            scp = None

if scp:
    try:
        scp.measure_mode = libtiepie.MM_STREAM
        scp.sample_frequency = 1e5
        scp.record_length = 100000
        scp.resolution = 16
        for ch in scp.channels:
            ch.enabled = True
            ch.range = 2
            ch.coupling = libtiepie.CK_DCV
            ch.safe_ground_enabled = True
            ch.safe_ground_threshold = 0.1
        
        command = 'SD1V' + str(drain) + '\r'
        ser.write('SD1V' + str(32699 + voltage/60) + '\r')
        print(ser.read(30))
        ser.write('SD2V32701\r')
        print(ser.read(30))
        ser.write('SD3V32768\r')
        print(ser.read(30))
        ser.write('SD4V32768\r')
        print(ser.read(30))
        ser.write('SG1V32769\r')
        print(ser.read(30))
        ser.write('SG2V32851\r')
        print(ser.read(30))
        ser.write('SG3V32804\r')
        print(ser.read(30))
        ser.write('SG4V32784\r')
        print(ser.read(30))
       
        #for i in xrange(n_steps):
         #   command = 'SD1V' + str(drain) + '\r'
          #  ser.write(command)
            
            #print(ser.read(5))
            #for j in xrange(n_steps):
             #   command = 'SD1V' + str(drain) + '\r'
              #  ser.write(command)
               # print(ser.read(5))
            
        scp.start()

        csv_file = open('/home/gamma-dna/Experiments/03.06.2019/Test.csv', 'w')
        try:
            csv_file.write('Sample')
            for i in range(len(scp.channels)):
                csv_file.write(';Ch' + str(i + 1))
            csv_file.write(os.linesep)
        
            sample = 0
            for chunk in range(n):
                while not (scp.is_data_ready or scp.is_data_overflow):
                    time.sleep(0.01)
                            
                if scp.is_data_overflow:
                    print('Data overflow!')
                    break
        
                data = scp.get_data()
        
                for i in range(len(data[0])):
                    csv_file.write(str(sample + i))
                    for j in range(len(data)):
                        csv_file.write(';' + str(data[j][i]))
                    csv_file.write(os.linesep)
        
                sample += len(data[0])
        finally:
            csv_file.close()
                
        scp.stop()    

    except Exception as e:
        print('Exception: ' + e.message)
        sys.exit(1)
    del scp

else:
    print('No oscilloscope available with stream measurement support!')
    sys.exit(1)

ser.close()
sys.exit(0)