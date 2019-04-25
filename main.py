from time import time
import pause
import sched
from hue_interface import HueOutput, get_number_lights, initialize
import librosa
import signal
from soundscraper import Tracker, Output
from audio_stream import audio_stream
from chroma_to_notes import get_notes
from get_componets import get_cmpnts
from midi_interface import MIDIOutput, initializeMIDI, getOutputs
from visualizer_interface import VisWindow, VisOutput

DETECT_COMPS = True

def main():
    trackers = []
    outputs = []
    song_name = "./test_music/piano.wav"

    # Load samples from file to be used with librosa
    print("Loading file...")
    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    scheduler = sched.scheduler(time, pause.seconds)

    # bridge = initialize()
    wind = VisWindow(500, 500, 16)
    midiPort = initializeMIDI(getOutputs()[-1])

    # Outputs
    num_outputs = 2
    for i in range(1, num_outputs + 1):
        outputs.append(MIDIOutput(midiPort, i))
    
    # Detect components and their activations
    if DETECT_COMPS:
        print("Detecting components...")
        comp_events = get_cmpnts(waveform, samplerate, num_outputs)
        for i in range(num_outputs):
            comp_tracker = Tracker([x for x in comp_events if int(x[0]) == i], outputs[i].handler)
            trackers.append(comp_tracker)
            comp_tracker.schedule(scheduler)
    else:    
        print("Detecting notes...")
        notes = get_notes(waveform, samplerate)
        note_tracker = Tracker([x for x in notes if x[0] in ["C", "C#", "D", "D#"]], outputs[0].handler)
        trackers.append(note_tracker)
        note_tracker.schedule(scheduler)
        note_tracker = Tracker([x for x in notes if x[0] in ["E", "F", "F#", "G"]], outputs[1].handler)
        trackers.append(note_tracker)
        note_tracker.schedule(scheduler)
        note_tracker = Tracker([x for x in notes if x[0] in ["G#", "A", "A#", "B"]], outputs[2].handler)
        trackers.append(note_tracker)
        note_tracker.schedule(scheduler)

    print("Starting track and running events...")
    song.start()
    scheduler.run()

if __name__ == "__main__":
    main()