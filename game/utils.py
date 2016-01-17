import os

def reverse_enumerate(List):
    return zip(reversed(range(len(List))), reversed(List))

def par_dir():
    "Returns parent directory for this project"
    return os.path.dirname(os.path.realpath(__file__ + "/..") )

class Timer(object):

    def __init__(self, interval, callback, call_limit=-1):

        self.interval = interval
        self.callback = callback
        self.call_limit = call_limit
        self.time = 0
        self.calls = 0
        self.active = True

    def update(self, time_passed):
        if not self.active:
            return

        self.time += time_passed

        if self.time >= self.interval:
            self.time -= self.interval
            self.calls += 1
            self.callback()

            if self.call_limit > -1 and self.calls >= self.call_limit:
                self.active = False
