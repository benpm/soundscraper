from time import time
import pause
import sched
from hue_interface import create_bridge_conn, set_light, flash_light
import librosa
from audio_stream import audio_stream
from chroma_to_notes import get_notes
from get_componets import get_cmpnts

DETECT_COMPS = True
DETECT_NOTES = False

class Tracker:
    def __init__(self, events, output_handler):
        "Events are a list of tuples: [(label, start, length), ...]"
        self.events = events
        self.output_handler = output_handler
    
    def schedule(self, scheduler):
        "Schedule my events in given scheduler, events are handled by my output handler"
        for event in self.events:
            scheduler.enter(event[1], 0, self.output_handler, argument=event)

def main():
    trackers = []
    song_name = "./test_music/test.wav"

    # Load samples from file to be used with librosa
    print("Loading file...")
    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    scheduler = sched.scheduler(time, pause.seconds)
    
    # Detect components and their activations
    if DETECT_COMPS:
        print("Detecting components...")
        comp_events = get_cmpnts(waveform, samplerate, 3)
        comp_tracker = Tracker(comp_events, print)
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