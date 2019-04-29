from soundscraper import Tracker, Output
from os import path
from time import sleep
from audio_stream import audio_stream
from chroma_to_notes import get_notes
from get_componets import get_cmpnts
import sched
from time import time
import librosa
import pause
import mido.ports
import random

NOTES = {
    "C": 72,
    "C#": 73,
    "D": 74,
    "D#": 75,
    "E": 76,
    "F": 77,
    "F#": 78,
    "G": 79,
    "G#": 80,
    "A": 81,
    "A#": 82,
    "B": 83
}

def getOutputs():
    return mido.get_output_names()

def initializeMIDI(outputName):
    return mido.open_output(outputName)

class MIDIOutput(Output):
    def __init__(self, port, index):
        self.port = port
        self.msg = mido.Message("note_on")
        self.msgoff = mido.Message("note_off")
    
    def handler(self, label, start_time, length):
        if label in NOTES.keys():
            self.msg.note = NOTES.get(label)
        else:
            self.msg.note = random.randint(50, 70)
        self.msg.channel = 0
        self.port.send(self.msg)
        sleep(0.05)
        self.msgoff.note = self.msg.note
        self.port.send(self.msgoff)

def run_song(song_name, port_name):
    port = initializeMIDI(port_name)

    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    scheduler = sched.scheduler(time, pause.seconds)

    # Outputs
    midi_output = MIDIOutput(port, 0)
    
    # Detect components and their activations
    print("Detecting notes...")
    notes = get_notes(waveform, samplerate)
    note_tracker = Tracker(notes, midi_output.handler)
    note_tracker.schedule(scheduler)

    print("Starting track and running events...")
    song.start()
    scheduler.run()