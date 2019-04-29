import librosa
import librosa.decompose
import numpy as np

"""
get_cmpnts, identifies unique audio components from audio data and determines when they occur
raw_audio, array of audio samples, presumed to be in mono (1 audio channel)
sample_rate, how man samples correspond to 1 second of real time (this is in hertz, NOT kilohertz)
num_cmpnts, how many unique audio components the data should be categorized into
returns, an array of 3-tuples detailing each occurence of a component, (component_name, start_time (in seconds), duration (in seconds))
"""
def get_cmpnts(raw_audio, sample_rate, num_cmpnts):
    stft = librosa.stft(raw_audio)
    spectrogram = np.abs(stft)
    
    components, activations = librosa.decompose.decompose(spectrogram, n_components=num_cmpnts)

    audio_length = len(raw_audio) / sample_rate
    precision = audio_length / activations.shape[1]

    threshold = 0.25
    
    max_vals = np.zeros(shape=num_cmpnts)
    for i in range(activations.shape[1]):
        for j in range(num_cmpnts):
            if(activations[j][i] > max_vals[j]):
                max_vals[j] = activations[j][i]

    activated = 0
    start = 0

    return_me = []
    for i in range(num_cmpnts):
        for j in range(activations.shape[1]):
            if(activations[i][j] >= threshold * max_vals[i] and activated == 0):
                activated = 1
                start = j * precision
            elif (activations[i][j] < threshold * max_vals[i] and activated == 1):
                activated = 0
                return_me.append((f'{i}', start, (j * precision) - start))

    return return_me