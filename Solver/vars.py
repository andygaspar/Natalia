class Ivars:
    def __init__(self, period):
        self.period = period
        self.inNeed = []
        self.available = []
        self.empty = True

    def add_in_need(self, acc):
        self.inNeed.append(acc)
        self.empty = False

    def add_available(self, acc):
        self.available.append(acc)