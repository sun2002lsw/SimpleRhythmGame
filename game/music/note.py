from etc import func


class Note:
    def __init__(self, beginSec, duration):
        self.BeginSec = beginSec
        self.EndSec = beginSec + duration
        self.Color = func.RandomBrightColor()
