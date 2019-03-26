from sched import scheduler

class Tracker:
    def __init__(self, events, output_handler):
        "Events are a list of tuples: [(label, start, length), ...]"
        self.events = events
        self.output_handler = output_handler
    
    def schedule(self, scheduler):
        "Schedule my events in given scheduler, events are handled by my output handler"
        for event in self.events:
            scheduler.enter(event[1], 0, self.output_handler, argument=event)

class Output:
    def __init__(self):
        pass
    
    def handler(self, label, start_time, length):
        raise NotImplementedError

class DummyOutput(Output):
    def __init__(self):
        super().__init__()
    
    def handler(self, label, start_time, length):
        print(label)
