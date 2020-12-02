import glob
import re
import numpy as np
import pandas as pd
import librosa
import csv


header = 'filename chroma_stft rms spectral_centroid spectral_bandwidth rolloff zero_crossing_rate onset_strength'
for i in range(1, 21):
    header += f' mfcc{i}'
header += f' label'

file = open('mfcc_data.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())


for wav_file in glob.glob(r".\chunked_audio_files_drunk\*.wav"):
    label = 0
    y, sr = librosa.load(wav_file)

    zero_crossing = librosa.feature.zero_crossing_rate(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    S, phase = librosa.magphase(librosa.stft(y))
    rolloff = librosa.feature.spectral_rolloff(S=S, sr=sr)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    allData = f'{wav_file} {np.mean(chroma)} {np.mean(rms)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zero_crossing)} {np.mean(onset_env)}'

    for number in mfcc:
        allData += f' {np.mean(number)}'

    allData += f' {label}'
    file = open('mfcc_data.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(allData.split())
