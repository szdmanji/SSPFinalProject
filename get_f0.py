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

header = 'filename f0 shimmer label'

file = open('f0_data_sober.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())

#get data
for wav_file in glob.glob(r"./chunked_audio_files_sober/*.wav"):
    label = 0
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)
    meanpitch = call(pitch, "Get mean", 0, 0, "Hertz")



    pointProcess = call([sound,pitch], "To PointProcess (periodic, cc)", 75, 600)
    shimmer_local = call([sound, pointProcess], "Get shimmer (local)...", 0.0, 0.0, 0.0001, 0.02, 1.3, 1.6)


    #intensity = call(sound, "To Intensity", 75, 0, "yes")
    #meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    #duration = call(sound, "Get total duration")

    theData = f'{wav_file} {meanpitch} {shimmer_local}'



    #formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    sober_f0.append(meanpitch)
    shimmer.append(shimmer_local)
    theData += f' {label}'
    file = open('f0_data_sober.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(theData.split())


