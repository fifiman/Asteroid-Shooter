

def reverse_enumerate(List):
    return zip(reversed(range(len(List))), reversed(List))


class Timer(object):

    def __init__(self, interval, callback, call_once=False):

        self.interval = interval
        self.callback = callback
        self.call_once = call_once
        self.time = 0
        self.active = True

    def update(self, time_passed):
        if not self.active:
            return

        self.time += time_passed

        if self.time >= self.interval:
            self.time -= self.interval
            self.callback()

            if self.call_once:
                self.active = False
