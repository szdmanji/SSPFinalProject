import glob
import re
import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd
import csv
import os

f1_list = []
f2_list = []
fratio_list = []

'''header = 'filename f1 f2'

file = open('test_formants.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())'''

#get data
for wav_file in glob.glob(r"./chunked_audio_files_drunk/*.wav"):
    label = 1
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)

    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 500)
    pulses = call([sound,pitch], "To PointProcess (cc)")
    shimmer_local = call([sound, pulses], "Get shimmer (local)...", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
    jitter_local = call(pulses, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)

    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5500, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')

        f1_list.append(f1)
        f2_list.append(f2)
        if isinstance(f1, float) == True:
            f1_list.append(f1)
        if isinstance(f2, float) == True:
            f2_list.append(f2)
        
        fratio = f1/f2
        fratio_list.append(fratio)
        

    '''theData = f'{wav_file}'
    
    theData += f' {label}'
    file = open('test_formants.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(theData.split())'''

print(fratio_list)