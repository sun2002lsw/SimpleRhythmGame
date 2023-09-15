class Sheet:
    def __init__(self):
        self._laneSheet = dict()

    def GetLaneCnt(self):
        return self._laneSheet.__len__()

    # 해당 번호의 라인에 노트를 추가
    def AddNote(self, laneNum, note):
        if laneNum not in self._laneSheet:
            self._laneSheet[laneNum] = []

        self._laneSheet[laneNum].append(note)

    # 각 라인별로 화면에 표시할 노트를 추출
    def ExtractDrawableNotes(self, laneNum, currentSec, dropSec):
        self._deleteOldNotes(laneNum, currentSec, dropSec)

        notes = self._laneSheet[laneNum]
        inScreenSec = currentSec + dropSec

        return [note for note in notes if note.BeginSec < inScreenSec]

    # 이미 지나쳐간 오래된 노트들 삭제
    def _deleteOldNotes(self, laneNum, currentSec, dropSec):
        notes = self._laneSheet[laneNum]
        outScreenSec = currentSec - dropSec / 2

        self._laneSheet[laneNum] = [note for note in notes if note.EndSec > outScreenSec]
