class Sheet:
    def __init__(self):
        self._laneSheet = dict(list())

    def GetLaneCnt(self):
        return self._laneSheet.__len__()

    # 해당 번호의 라인에 노트를 추가
    def AddNote(self, laneNum, note):
        self._laneSheet[laneNum].append(note)

    # 각 라인별로 화면에 표시할 노트를 추출
    def ExtractDrawableNotes(self, dropSec, currentSec):
        self._deleteOldNotes(dropSec, currentSec)

        inScreenSec = currentSec + dropSec

        laneNotes = dict(list())
        for laneNum, notes in self._laneSheet.items():
            drawableNotes = [note for note in notes if note.BeginSec < inScreenSec]
            laneNotes[laneNum] = drawableNotes

        return laneNotes

    # 이미 지나쳐간 오래된 노트들 삭제
    def _deleteOldNotes(self, dropSec, currentSec):
        outScreenSec = currentSec - dropSec / 2

        for laneNum, notes in self._laneSheet.items():
            remainNotes = [note for note in notes if note.EndSec < outScreenSec]
            self._laneSheet[laneNum] = remainNotes
