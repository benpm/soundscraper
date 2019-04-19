from soundscraper import Output
from os import path
import random
from time import sleep
import mido.ports

class MIDIOutput(Output):
    def __init__(self):
        self.port = mido.open_output(mido.get_output_names()[-1])
        self.msg = mido.Message("note_on")
    
    def handler(self, label, start_time, length):
        self.msg.note = random.randint(40, 110)
        self.msg.channel = 0
        self.port.send(self.msg)