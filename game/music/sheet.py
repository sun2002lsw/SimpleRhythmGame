from .note import Note


class Sheet:
    def __init__(self):
        self._laneNotes = dict()

    def GetLaneNotes(self):
        initNote = Note(0, 0)

        self._AddNote(0, initNote)
        self._AddNote(1, initNote)
        self._AddNote(2, initNote)
        self._AddNote(3, initNote)

        note1 = Note(1, 3)
        self._AddNote(0, note1)
        self._AddNote(3, note1)

        note2 = Note(2, 1)
        self._AddNote(1, note2)

        note3 = Note(2.5, 2)
        self._AddNote(2, note3)

        note4 = Note(4, 3)
        self._AddNote(3, note4)

        return self._laneNotes

    # 해당 번호의 라인에 노트를 추가
    def _AddNote(self, laneNum, note):
        if laneNum not in self._laneNotes:
            self._laneNotes[laneNum] = []

        self._laneNotes[laneNum].append(note)
