import glob
import parselmouth
from parselmouth.praat import call
import csv

header = 'filename f1 f2 f1/f2_ratio'

file = open('test_formants_drunk.csv', 'w', newline='')
with file:
    writer = csv.writer(file)
    writer.writerow(header.split())

#get data
for wav_file in glob.glob(r"./chunked_audio_files_drunk/*.wav"):
    label = 0
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)

    pointProcess = call(sound, "To PointProcess (periodic, cc)", 75, 500)

    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5500, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')

        fratio = f1/f2

    theData = f'{wav_file} {f1} {f2} {fratio}'
    theData += f' {label}'

    file = open('test_formants_drunk.csv', 'a', newline='')
    with file:
        writer = csv.writer(file)
        writer.writerow(theData.split())
