from enum import Enum, auto


class Note:
    def __init__(self, beginSec, duration):
        self.BeginSec = beginSec
        self.EndSec = beginSec + duration
        self.State = NoteState.Drop


class NoteState(Enum):
    Drop = auto()   # HitLine을 향해서 떨어지고 있음
    Hit = auto()    # HitLine에서 타이밍 맞게 눌러 맞춤
    Miss = auto()   # 멍 때리다 놓침
