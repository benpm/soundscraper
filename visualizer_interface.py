from soundscraper import Output
from time import sleep
from graphics import GraphWin, Rectangle, Point, color_rgb

"""class HueOutput(Output):
    def __init__(self, bridge, light_index):
        super().__init__()

    def handler(self, label, pythostart_time, length):"""

class VisWindow():
    def __init__(self, win_w, win_h, num_rects):
        self.win = GraphWin("Visualizer", win_w, win_h)
        self.rect_array = []
        for i in range(num_rects):
            r = Rectangle(Point(0, (i * win_h / 4)), Point(win_w, ((i + 1) * win_h / 4)))
            r.setFill(color_rgb(int(255 /num_rects * i), int(255 /num_rects * i), int(255 /num_rects * i)))
            self.rect_array.append(r)

class VisOutput(Output):
    def __init__(self, window, index):
        super().__init__()

        self.win = window.win
        self.rectangles = window.rectangles
        self.index = index

    def handler(self, label, start, length):
        self.rectangles[self.index].draw(self.win)
        sleep(0.01)
        self.rectangles[self.index].undraw()

#win.getMouse() # Pause to view result
#win.close()    # Close window when done
