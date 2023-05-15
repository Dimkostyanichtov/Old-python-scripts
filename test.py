#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:35:07 2019

@author: gamma-dna
"""
from __future__ import print_function
import time
import os
import sys
import libtiepie, struct, bitstring


# Print library info:


# Search for devices:
libtiepie.device_list.update()

# Try to open an oscilloscope with stream measurement support:
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
        # Set measure mode:
        scp.measure_mode = libtiepie.MM_STREAM

        # Set sample frequency:
        scp.sample_frequency = 1e5  # 1 kHz

        # Set record length:
        scp.record_length = 30000  # 1 kS
        
        scp.resolution = 16

        # For all channels:
        for ch in scp.channels:
            # Enable channel to measure it:
            ch.enabled = True

            # Set range:
            ch.range = 0.4  # 8 V

            # Set coupling:
            ch.coupling = libtiepie.CK_DCV  # DC Volt



        # Start measurement:
        scp.start()

        csv_file = open('OscilloscopeStream.csv', 'w')
        try:
            csv_file.write('Sample')
            for i in range(len(scp.channels)):
                csv_file.write(';Ch' + str(i + 1))
            csv_file.write(os.linesep)


            print()
            sample = 0
            for chunk in range(20):

                while not (scp.is_data_ready or scp.is_data_overflow):
                    time.sleep(0.01)

                if scp.is_data_overflow:
                    print('Data overflow!')
                    break

                data = scp.get_data()
                #for i in xrange(len(data)):
                    #for j in xrange(len(data[i])):
                        #print(bitstring.BitArray(float=data[i][j], length=32))
                        
                for i in xrange(len(data[0]) - 1):
                    point_1 = round(data[0][i], 1)
                    point_2 = round(data[0][i + 1], 1)
                    if point_1 == 0.4 and point_2 == 0.4 or point_1 == -0.4 and point_2 == -0.4:
                        scp.stop()
                        for ch in scp.channels:
                            ch.range = 0.8
                        scp.start()
                        break
                    else:
                        continue

                for i in range(len(data[0])):
                    csv_file.write(str(sample + i))
                    for j in range(len(data)):
                        csv_file.write(';' + str(data[j][i]))
                    csv_file.write(os.linesep)

                sample += len(data[0])

            print()
            print('Data written to: ' + csv_file.name)
        finally:
            csv_file.close()

        scp.stop()
        
    except 1:
        1



    del scp

else:
    print('No oscilloscope available with stream measurement support!')

sys.exit(0)