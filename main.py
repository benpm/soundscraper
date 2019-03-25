from random import randint
from time import time
import pause
import sched
from hueInterface import createBridgeConn, setLight, flashLight
import librosa
from audioStream import AudioStream
from chroma_to_notes import getNotes

def main():
    song_name = "piano.wav"

    print("Loading file...")
    audioStream = AudioStream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    
    print("Detecting beats...")
    tempo, beat_frames = librosa.beat.beat_track(waveform, samplerate)
    
    print("Converting beat sample idices to times...")
    # beat_times = librosa.frames_to_time(beat_frames, samplerate)
    notes = getNotes(waveform, samplerate)

    scheduler = sched.scheduler(time, pause.seconds)

    # # for sec, index in zip(beat_times, range(len(beat_times))):
    for note in notes: # note is (label, start, length)
        # scheduler.enter(sec, 1, flashLight, argument=(lights, index % 3 + 1), kwargs={'hue': randint(0, 65535)})
        scheduler.enter(note[1], 0, print, argument=note[0])

    print("Starting track and running events...")
    audioStream.start()
    scheduler.run()

def sync_function(note):
    print(note[0])

if __name__ == "__main__":
    main()