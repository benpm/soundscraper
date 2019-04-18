from soundscraper import Output
from os import path
import random
from time import sleep
import mido.ports

class MIDIOutput(Output):
    def __init__(self):
        self.port = mido.open_output()
    
    def handler(self, label, start_time, length):
        raise NotImplementedError