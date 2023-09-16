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

    # 각 라인별로 화면에 표시할 만큼 가까운 노트를 추출
    def ExtractVisibleNotes(self, currentSec, dropSec):
        self._deleteOldNotes(currentSec, dropSec)

        closeNotes = dict()
        inScreenSec = currentSec + dropSec

        for laneNum, notes in self._laneSheet.items():
            closeNotes[laneNum] = [note for note in notes if note.BeginSec < inScreenSec]

        return closeNotes

    # 이미 지나쳐간 오래된 노트들 삭제
    def _deleteOldNotes(self, currentSec, dropSec):
        outScreenSec = currentSec - dropSec / 2

        for laneNum, notes in self._laneSheet.items():
            self._laneSheet[laneNum] = [note for note in notes if note.EndSec > outScreenSec]
