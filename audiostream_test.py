import librosa
import wave
import pyaudio
import time
import sys

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

samples, rate = librosa.load("music.wav", mono=True)

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# open stream using callback (3)
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=rate,
                output=True)

# start the stream (4)
stream.write(samples)

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()
