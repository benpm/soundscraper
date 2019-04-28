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
            #r.setFill(color_rgb(int(255 /num_rects * i), int(255 /num_rects * i), int(255 /num_rects * i)))
            r.draw(self.win)
            self.rectangles.append(r)

class VisOutput(Output):
    def __init__(self, window, index):
        super().__init__()

        self.win = window.win
        self.rectangles = window.rectangles
        self.index = index

    def handler(self, label, start, length):
        self.rectangles[self.index - 1].setFill(color_rgb(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        #sleep(0.075)
        #self.rectangles[self.index - 1].undraw()

#win.getMouse() # Pause to view result
#win.close()    # Close window when done
