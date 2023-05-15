"""
LSPone_example.py
~~~~~~~~~~~~~~~~~
This program shows how to connect to to the LSPone (laboratory syringe pump) using python.
The different commands can be found in the user manual.

:copyright: (c) 2017, E. Collot
:license: Proprietary, see LICENSE for details.

"""
#include python libraries
import sys
import serial
import time

# Open serial connection -> check COM port on your device
lsp = serial.Serial('COM3', 9600, timeout=1000)
print('LSPone connected on ',lsp.name)

# Initialise LSPone
lsp.write(b"/1ZR\r")
time.sleep(30)
print("LSP one ready")

# The command string can be generated using the LSPoneQuick software.
command = "/1V300M1000O4M1000A1200M1000V80O5M200A2400M1000V150O3M100A0R\r"
lsp.write(b"/1V300M1000O3M1000A2400M1000V80O5M200A0R\r")
time.sleep(32)

#Here is the detail of the sequence
# /1 	- command start
# V300 	- choose speed: 300 steps/s
# M1000 - 1000 ms delay, to ensure the next command will be executed correctly
# O3 	- go to port 3, clockwise rotation
# M1000 - 1000 ms delay
# A2400 - go to the absolute position 2400 (when controlled with absolute position, 
# 		  one does not need to pay special attention to the syringe that is mounted 
#		  on the pump)
# M1000 - 1000 ms delay
# V80 	- set speed to 80 steps/s
# O5 	- switch to port 5, clockwise rotation
# M200 	- 200 ms delay
# A0 	- go to absolute position 0 (= empty syringe)
# R 	- command end

#Finishing the script 
sys.exit(0)

