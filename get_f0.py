import glob
import re
import parselmouth
from parselmouth.praat import call
import numpy as np

drunk_f0 = []
sober_f0 = []


for wav_file in glob.glob(r".\chunked_audio_files_drunk\*.wav"):
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)
    meanpitch = call(pitch, "Get mean", 0, 0, "Hertz")
    intensity = call(sound, "To Intensity", 75, 0, "yes")
    meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    duration = call(sound, "Get total duration")

    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    parselmouth.praat.call(pitch_tier, "Save as PitchTier spreadsheet file", "drunkPitchTier.PitchTier")

    formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    drunk_f0.append(meanpitch)



for wav_file in glob.glob(r".\chunked_audio_files_sober\*.wav"):
    sound = parselmouth.Sound(wav_file)
    pitch = call(sound, "To Pitch", 0, 75, 600)
    meanpitch = call(pitch, "Get mean", 0, 0, "Hertz")
    intensity = call(sound, "To Intensity", 75, 0, "yes")
    meanintensity = call(intensity, "Get mean", 0, 0, "energy")
    duration = call(sound, "Get total duration")

    manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
    pitch_tier = call(manipulation, "Extract pitch tier")
    parselmouth.praat.call(pitch_tier, "Save as PitchTier spreadsheet file", "soberPitchTier.PitchTier")

    formant = call(sound, "To Formant (burg)", 0, 5, 5500, 0.025, 50)

    sober_f0.append(meanpitch)


