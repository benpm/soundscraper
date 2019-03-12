from pydub import AudioSegment
import librosa
import librosa.display
import librosa.decompose
import librosa.feature
import librosa.effects
from matplotlib import pyplot
from matplotlib import rc
import numpy

# Load audio sample
raw_audio, sample_rate = librosa.load("music.wav", mono=True)

# Generate spectrogram
stft_audio = librosa.stft(raw_audio)
spectrogram = numpy.abs(stft_audio)
components, activations = librosa.decompose.decompose(spectrogram, n_components=3)
scaled_spec = librosa.amplitude_to_db(spectrogram, ref=numpy.max)
y_harmonic, y_percussive = librosa.effects.hpss(raw_audio)
chromagram = librosa.feature.chroma_cqt(y_harmonic, sample_rate)

# Display stuff
plot_title_style = {"size": 8}
rc("font", **plot_title_style)
pyplot.style.use("dark_background")
pyplot.subplot(311)
pyplot.title("Spectrogram")
librosa.display.specshow(
	scaled_spec,
	y_axis="log", x_axis="time")
pyplot.subplot(323)
pyplot.title("Activations")
librosa.display.specshow(
	activations,
	x_axis="time")
pyplot.subplot(324)
pyplot.title("Components")
librosa.display.specshow(
	components,
	y_axis="log")
pyplot.subplot(313)
pyplot.title("Chromagram")
librosa.display.specshow(
	chromagram,
	x_axis="time", y_axis="chroma")

pyplot.show()
pyplot.tight_layout()
