# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import visa, io, json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter
from scipy.signal import freqz

rm = visa.ResourceManager()
instr = rm.open_resource('ASRL/dev/ttyACM0::INSTR')
instr.write('CHAN1:DATA:POIN MAX')
print(instr.query('CHAN1:DATA:POIN?'))

x = []
x.append(instr.query('CALC:QMAT:DATA?').split(','))
for i in xrange(len(x)):
    for j in xrange(len(x[i])):
        x[i][j] = round(float(x[i][j]), 6)
x = np.array(x)
fig, ax = plt.subplots()
y = list(range(1, (len(x[0])+1)))
ax.plot(y, x[0])
plt.grid(True)
ax.legend()
plt.show()

with io.open('/home/gamma-dna/Desktop/12.txt', 'w', encoding='utf8') as outfile:
    for  line in xrange(3000):
        outfile.write(unicode(str(x[0][line])) + '\n')

lowcut = 500.0
highcut = 1500000.0
fs = 30000000.0
order = 3

def butter_bandpass(lowcut, highcut, fs, order=6):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

b, a = butter_bandpass(lowcut, highcut, fs, order=order)

w, h = freqz(b, a, worN=2000)
plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)], '--', label='sqrt(0.5)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=6):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

y = butter_bandpass_filter(x, lowcut, highcut, fs, order=6)

fig, ax = plt.subplots()
y1 = list(range(1, (len(y[0])+1)))
ax.plot(y1, y[0])
plt.grid(True)
ax.legend()
plt.show()