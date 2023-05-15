#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:22:05 2019

@author: gamma-dna
"""
import sys, yaml, libtiepie, time

data = []

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

        scp.measure_mode = libtiepie.MM_STREAM
        scp.sample_frequency = 1e6
        scp.record_length = 10000000  # 1 kS
        scp.resolution = 16
    
        for ch in scp.channels:
            # Enable channel to measure it:
            ch.enabled = True

            # Set range:
            ch.range = 8  # 8 V

            # Set coupling:
            ch.coupling = libtiepie.CK_DCV  # DC Volt
            ch.safe_ground_enabled = True
            ch.safe_ground_threshold = 0.1


        # Start measurement:
        scp.start()
        
            # Measure 10 chunks:
        sample = 0
        for chunk in range(1):
            print(chunk)
                # Print a message, to inform the user that we still do something:
                #print('Data chunk ' + str(chunk + 1))

                # Wait for measurement to complete:
            while not (scp.is_data_ready or scp.is_data_overflow):
                time.sleep(0.01)  # 10 ms delay, to save CPU time

            if scp.is_data_overflow:
                print('Data overflow!')
                break

                # Get data:
            data.append(scp.get_data())

            sample += len(data[0])

        # Stop stream:
        scp.stop()

    except Exception as e:
        print('Exception: ' + e.message)
        sys.exit(1)
    
    to_yaml = {'data': data}
    with open('/home/gamma-dna/Experiments/data.yaml', 'w') as outfile:
        #outfile.write('description: Секвенирование олига VB15. Обеднение нуклеотидов в 100 раз.\n' + 'sequenceLength: 177\n' + 
         #             'bridge: "ACTGACTGACTGACTGACTGACTGA"\n' + 'aDelays:\n')
        yaml.dump(to_yaml, outfile, default_flow_style=False)

    # Close oscilloscope:
    del scp
        
else:
    print('No oscilloscope available with stream measurement support!')
    sys.exit(1)

sys.exit(0)