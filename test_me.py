from pydub import AudioSegment
import librosa
from matplotlib import pyplot
import numpy

raw_audio, sample_rate = librosa.load("wilhelm.wav", mono=True)
print("Number of samples in audio data = %d" % len(raw_audio))

transformed_audio = librosa.stft(raw_audio, dtype=numpy.float)
print(type(transformed_audio))
pyplot.imshow(transformed_audio)
pyplot.show()
