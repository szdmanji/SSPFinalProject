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

header = 'filename f0 label'

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
    #intensity = call(sound, "To Intensity", 75, 0, "yes")
    #meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    #duration = call(sound, "Get total duration")
    thePitch = f'{wav_file} {meanpitch}'



    #formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    sober_f0.append(meanpitch)
    thePitch += f' {label}'
    file = open('f0_data_sober.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(thePitch.split())


