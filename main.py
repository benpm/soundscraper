from time import time
import pause
import sched
from hue_interface import HueOutput, get_number_lights
import librosa
import signal
from soundscraper import Tracker, Output
from audio_stream import audio_stream
from chroma_to_notes import get_notes
from get_componets import get_cmpnts

DETECT_COMPS = True
DETECT_NOTES = False

def main():
    trackers = []
    outputs = []
    song_name = "./test_music/test.wav"

    # Load samples from file to be used with librosa
    print("Loading file...")
    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    scheduler = sched.scheduler(time, pause.seconds)

    # Outputs
    num_outputs = 5
    for i in range(num_outputs):
        outputs.append(HueOutput())
    
    # Detect components and their activations
    if DETECT_COMPS:
        print("Detecting components...")
        comp_events = get_cmpnts(waveform, samplerate, num_outputs)
        for i in range(num_outputs):
            comp_tracker = Tracker([x for x in comp_events if int(x[0]) == i], outputs[i].handler)
            trackers.append(comp_tracker)
            comp_tracker.schedule(scheduler)
    
    # Detect notes and their activations
    if DETECT_NOTES:
        print("Detecting notes...")
        notes = get_notes(waveform, samplerate)
        note_tracker = Tracker(notes, print)
        trackers.append(note_tracker)
        note_tracker.schedule(scheduler)

    print("Starting track and running events...")
    song.start()
    scheduler.run()

if __name__ == "__main__":
    main()