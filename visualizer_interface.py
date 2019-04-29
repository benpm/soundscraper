from soundscraper import Output
from time import sleep
from graphics import GraphWin, Rectangle, Point, color_rgb
import random
"""class HueOutput(Output):
    def __init__(self, bridge, light_index):
        super().__init__()

    def handler(self, label, pythostart_time, length):"""

class VisWindow():
    def __init__(self, win_w, win_h, num_rects):
        self.win = GraphWin("Visualizer", win_w, win_h)
        self.rectangles = []
        
        rect_height = win_h / num_rects
        rect_width = win_w
        for i in range(num_rects):
            r = Rectangle(Point(0, i * rect_height), Point(rect_width, (i + 1) * rect_height))
            r.draw(self.win)
            self.rectangles.append(r)

class VisOutput(Output):
    def __init__(self, window, index):
        super().__init__()

        self.win = window.win
        self.rectangles = window.rectangles
        self.index = index
        self.colors = ["red", "blue", "green"]
        self.color_index = index % 3
        
    def handler(self, label, start, length):
        self. color_index = (color_index + 1) % 3
        self.rectangles[self.index - 1].setFill(self.colors[self.color_index])

def runMain(audio_path, num_outputs, detect_comps):
    trackers = []
    outputs = []
    song_name = audio_path

    # Load samples from file to be used with librosa
    print("Loading file...")
    song = audio_stream(song_name)
    waveform, samplerate = librosa.load(song_name, sr=None)
    scheduler = sched.scheduler(time, pause.seconds)

    # bridge = initialize()
    # midiPort = initializeMIDI(getOutputs()[-1])

    # Outputs
    wind = VisWindow(1000, 1000, num_outputs)
    for i in range(1, num_outputs + 1):
        outputs.append(VisOutput(wind, i))
    
    # Detect components and their activations
    if detect_comps:
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
