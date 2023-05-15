#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 12:57:43 2019

@author: gamma-dna
"""

import wave, matplotlib, json, io
import numpy as np
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

wav = wave.open("/home/gamma-dna/Downloads/Tran 6 ch 1 drain 30 mV gate 1,8 V pulse 5 mV 10 MHz_01_CLEARED (1).wav", mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
w, h = 800, 300
k = nframes/w/32
DPI = 72
peak = 256 ** sampwidth / 2
samp = []
threshhold = 10000.0
res = []
zeros = 0
num = 0

content = wav.readframes(nframes)
samples = np.frombuffer(content, dtype=types[sampwidth])
samples.setflags(write = 1)
for i in xrange(len(samples)):
    samp.append(float(samples[i]))

n = np.arange(len(samples))
fig, ax = plt.subplots()
ax = plt.plot(n, samples, label=u'Форма сигнала')
plt.xlabel('x')
plt.ylabel('f (x)')
plt.legend(loc='best')
plt.show()
    
for i in xrange(10000, len(samp) - 10000):
    if samp[i] < threshhold:
        zeros += 1
    elif samp[i] >= threshhold and zeros != 0 and zeros > 3 and num + 10000 < i:
        res.append(zeros)
        zeros = 0
        num = i
    else:
        continue

print(len(res), res)

writefilename = '/home/gamma-dna/Experiments/delays.json'

json_string = {'Research data': res}
with io.open(writefilename, 'w') as outfile:
    str_ = json.dumps(json_string,
                      indent=4, sort_keys=False,
                      separators=(',', ': '), ensure_ascii = True)
    outfile.write(unicode(str_))
    