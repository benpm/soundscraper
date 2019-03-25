from time import time
import pause
import sched
from hue_interface import create_bridge_conn, set_light, flash_light
import librosa
from audio_stream import audio_stream
from chroma_to_notes import get_notes

def main():
    song_name = "./test_music/tones.wav"

    print("Loading file...")
    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    
    # print("Detecting notes...")
    # tempo, beat_frames = librosa.beat.beat_track(waveform, samplerate)
    
    # print("Converting beat sample idices to times...")
    # beat_times = librosa.frames_to_time(beat_frames, samplerate)
    
    print("Detecting notes...")
    notes = get_notes(waveform, samplerate)

    scheduler = sched.scheduler(time, pause.seconds)

    for note in notes: # note is (label, start, length)
        scheduler.enter(note[1], 0, print, argument=note[0])

    print("Starting track and running events...")
    song.start()
    scheduler.run()

if __name__ == "__main__":
    main()