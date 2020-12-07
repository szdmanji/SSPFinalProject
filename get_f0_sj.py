import glob
import re
import parselmouth
from parselmouth.praat import call
import numpy as np
import pandas as pd
import csv
import os

drunk_f0 = []
sober_f0 = []
shimmer = []
jitter = []
#f1_list = []
#f2_list = []
#fratio_list = []
'''manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
pitch_tier = call(manipulation, "Extract pitch tier")
parselmouth.praat.call(pitch_tier, "Save as PitchTier spreadsheet file", "drunkPitchTier.PitchTier")

manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
pitch_tier = call(manipulation, "Extract pitch tier")
parselmouth.praat.call(pitch_tier, "Save as PitchTier spreadsheet file", "soberPitchTier.PitchTier")
'''

'''
#get drunk data
for wav_file in glob.glob(r".\chunked_audio_files_drunk\*.wav"):
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)
    meanpitch = call(pitch, "Get mean", 0, 0, "Hertz")
    intensity = call(sound, "To Intensity", 75, 0, "yes")
    meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    duration = call(sound, "Get total duration")


   

    formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    drunk_f0.append(meanpitch)
'''

header = 'filename f0 shimmer jitter label'

file = open('f0_data_drunk.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())

#get data
for wav_file in glob.glob(r"./chunked_audio_files_drunk/*.wav"):
    label = 1
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)
    meanpitch = call(pitch, "Get mean", 0, 0, "Hertz")


    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 500)
    pulses = call([sound,pitch], "To PointProcess (cc)")
    shimmer_local = call([sound, pulses], "Get shimmer (local)...", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)
    jitter_local = call(pulses, "Get jitter (local)", 0.0, 0.0, 0.0001, 0.02, 1.3)

    '''formants = call(sound, "To Formant (burg)", 0.0025, 5, 5500, 0.025, 50)
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
        fratio_list.append(fratio)'''

    #intensity = call(sound, "To Intensity", 75, 0, "yes")
    #meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    #duration = call(sound, "Get total duration")

    theData = f'{wav_file} {meanpitch} {shimmer_local} {jitter_local}'



    #formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    drunk_f0.append(meanpitch)
    shimmer.append(shimmer_local)
    jitter.append(jitter_local)

    theData += f' {label}'
    file = open('f0_data_drunk.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(theData.split())


