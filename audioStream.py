import simpleaudio as sa
from threading import Thread

class AudioStream(Thread):
    """Class to stream audio during event execution"""
    def __init__(self, audioPath):
        """
            This is a threading object representing an audio stream. 
            To run the audio stream for AudioStream obj named 'astream',
            call astream.start(), NOT astream.run(). 
            This is !!!!!NON BLOCKING!!!!!
        """
        Thread.__init__(self)
        
        self.wav = sa.WaveObject.from_wave_file(audioPath)
    
    def run(self):
        """ 
            Starts audio. Should be called with obj.start() not obj.run()
            This is !!!!!NON BLOCKING!!!!!
        """
        play_obj = self.wav.play()
        play_obj.wait_done()

