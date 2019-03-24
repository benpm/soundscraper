import librosa
import numpy
import wave
import pyaudio
import time
import sys

position = 0

def stream_callback(in_data, frame_count, time_info, status):
    return (samples, pyaudio.paContinue)

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

CHUNK = 1024
samples, rate = librosa.load("music.wav", mono=True)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream using callback (3)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=rate,
                output=True,
                stream_callback=stream_callback)

# start the stream (4)
#stream.write(samples, len(samples))
stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()
