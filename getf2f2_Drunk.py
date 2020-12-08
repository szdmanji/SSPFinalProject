import glob, re, os, numpy as np
import parselmouth, matplotlib.pyplot as plt
import csv
from os.path import join
from collections import Counter
from parselmouth.praat import call



# FILEPATH = '/Users/ramzibishtawi/Documents/CSCI-3398/SSPFinalProject'

# function to get features for a .wav file
def getFeatures(wav_file):
    # get duration, mean pitch, mean intensity
    sound = parselmouth.Sound(wav_file)

    formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
    # tg_file = re.sub("wav", "TextGrid", wav_file)
    # textgrid = call("Read from file", tg_file)
    # intv = call(textgrid, "Get number of intervals", 1)

    vowels = 0
    f1_vowels = 0
    f2_vowels = 0

    # for each interval/phoneme
    for i in range(1, intv):
        phone = call(textgrid, "Get label of interval", 1, i)
        # vowels
        if phone == 'sil': continue
        if re.match('[AEIOU](?![LMR])', phone):
            vowels += 1
            vowel_onset = call(textgrid, "Get starting point", 1, i)
            vowel_offset = call(textgrid, "Get end point", 1, i)
            midpoint = vowel_onset + ((vowel_offset - vowel_onset) / 2)
            # get features
            f1_vowels += call(formant, "Get value at time", 1, midpoint, "Hertz", "Linear")
            f2_vowels += call(formant, "Get value at time", 2, midpoint, "Hertz", "Linear")


    f1_vowels = f1_vowels / vowels if vowels > 0 else 0
    f2_vowels = f2_vowels / vowels if vowels > 0 else 0
    fratio = f1_vowels / f2_vowels

    results = [
                f1_vowels,
                f2_vowels,
                fratio
            ]

    return results

### GET DRUNK DATA

# list to store drunk features
drunk = []
counter = 0

header = 'filename f1/f2 label'

file = open('f1_f2_data_drunk.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())
# for each .wav file
print(1)
for wav_file in glob.glob(r"./chunked_audio_files_drunk/*.wav"):
    print(1)
    label = 0
    # print progress
    counter += 1
    if counter % 100 == 0:
        print(counter, wav_file)

    # get features
    results = getFeatures(wav_file)
    # append all the features to the drunk data
    drunk.append(results)




    theData = f'{wav_file} {results}'
    theData += f' {label}'
    file = open('f1/f2_data_drunk.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(theData.split())
