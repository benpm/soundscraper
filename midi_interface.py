from soundscraper import Output
from os import path
import random
from time import sleep
import mido.ports

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
    
    def handler(self, label, start_time, length):
        if label in NOTES.keys():
            self.msg.note = NOTES.get(label)
        else:

        self.msg.channel = 0
        self.port.send(self.msg)