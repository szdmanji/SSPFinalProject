import glob, re, os, numpy as np
import parselmouth, matplotlib.pyplot as plt
from os.path import join
from collections import Counter
from parselmouth.praat import call
from sklearn import metrics
from sklearn.model_selection import cross_validate
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier

FILEPATH = '/Users/ramzibishtawi/Documents/CSCI-3398/SSPFinalProject'

# function to get features for a .wav file
def getFeatures(wav_file):
    # get duration, mean pitch, mean intensity
    sound = parselmouth.Sound(wav_file)

    formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)
    tg_file = re.sub("wav", "TextGrid", wav_file)
    textgrid = call("Read from file", tg_file)
    intv = call(textgrid, "Get number of intervals", 1)
    
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

    results = [
                f1_vowels,
                f2_vowels,
            ]
   
    return results

### GET Drunk DATA

# list to store Drunk features
drunk = []
counter = 0 

# for each .wav file
for wav_file in glob.glob(join(FILEPATH, "\chunked_audio_files_drunk/*.wav")):
    
    # print progress
    counter += 1
    if counter % 100 == 0:
        print(counter, wav_file)
    
    # get features
    results = getFeatures(wav_file)
    # append all the features to the drunk data 
    drunk.append(results)


