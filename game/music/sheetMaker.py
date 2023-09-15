from .note import *
from .sheet import *


class SheetMaker:
    def __init__(self):
        pass

    def MakeSheet(self):
        s = Sheet()

        initNote = Note(0, 0)

        s.AddNote(0, initNote)
        s.AddNote(1, initNote)
        s.AddNote(2, initNote)
        s.AddNote(3, initNote)

        note1 = Note(1, 3)
        s.AddNote(0, note1)
        s.AddNote(3, note1)

        note2 = Note(2, 1)
        s.AddNote(1, note2)

        note3 = Note(4, 3)
        s.AddNote(3, note3)

        return s