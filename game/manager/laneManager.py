from .effectManager import *
from ..music.note import NoteState


class LaneManager:
    def __init__(self, screen, laneLeftX, laneWidth, laneBottomY, hitLineY, notes, noteColor, noteDropSec):
        self._screen = screen
        self._laneLeftX = laneLeftX
        self._laneWidth = laneWidth
        self._laneBottomY = laneBottomY
        self._hitLineY = hitLineY
        self._notes = notes
        self._noteColor = noteColor
        self._noteDropSec = noteDropSec
        self._isPressing = False

        # 이펙트 관리자
        self._effectManager = EffectManager(screen, laneLeftX, laneWidth, hitLineY)

        # 노트의 x 위치와 너비
        leftMargin = self._laneWidth * 0.1
        self._noteWidth = self._laneWidth - 2 * leftMargin
        self._noteWidth += self._laneWidth / 30  # 선 굵기 때문에 width 살짝 부족하다;;
        self._noteLeftX = self._laneLeftX + leftMargin

    # 놓치는 노트 확인
    def CheckMiss(self, currentSecond):
        for i, note in enumerate(self._notes):
            if note.BeginSec > currentSecond + 0.3:
                break  # 여기 i 부터는 아직 확인할 필요 없는 노트

            if note.State == NoteState.Drop:
                if currentSecond - 0.3 < note.BeginSec < currentSecond:
                    self._effectManager.Start(EffectType.Danger)
                if note.BeginSec < currentSecond - 0.3:
                    self._notes[i].State = NoteState.Miss
                    self._effectManager.Start(EffectType.Miss)

    def SetNoteDropSec(self, noteDropSec):
        self._noteDropSec = noteDropSec

    def HandleKeyDown(self):
        self._isPressing = True

    def HandleKeyUp(self):
        self._isPressing = False

    # 해당 라인의 상황 그리기
    def Draw(self, currentSecond):
        self._DrawInput()
        self._DrawNotes(currentSecond)
        self._effectManager.Draw()

    # 키를 눌렀을 때 효과 그리기
    def _DrawInput(self):
        if self._isPressing:
            for i in range(0, 200):
                color = (i, i, i)
                y = self._laneBottomY - i
                startPos = (self._noteLeftX, y)
                endPos = (self._noteLeftX + self._noteWidth - 1, y)

                pygame.draw.line(self._screen, color, startPos, endPos)

            for i in range(0, 200):
                color = (200 - i, 200 - i, 200 - i)
                y = self._laneBottomY - 200 - i
                startPos = (self._noteLeftX, y)
                endPos = (self._noteLeftX + self._noteWidth - 1, y)

                pygame.draw.line(self._screen, color, startPos, endPos)

    # 각 노트들 그리기
    def _DrawNotes(self, currentSecond):
        self._DelOutOfScreenNote(currentSecond)

        inTheScreenSec = currentSecond + self._noteDropSec
        visibleNotes = [note for note in self._notes if note.BeginSec < inTheScreenSec]

        for note in visibleNotes:
            topY, height = self._CalcNotePosY(currentSecond, note)
            noteRect = (self._noteLeftX, topY, self._noteWidth, height)
            pygame.draw.rect(self._screen, self._noteColor, noteRect)

    # 화면 밖으로 사라진 노트 지우기
    def _DelOutOfScreenNote(self, currentSecond):
        if len(self._notes) == 0:
            return

        outOfScreenSec = currentSecond - self._noteDropSec

        if self._notes[0].EndSec < outOfScreenSec:
            self._notes.pop(0)

    # 해당 노트 second 맞는 y 위치와 길이 찾기
    def _CalcNotePosY(self, currentSecond, note):
        beginRemainSec = note.BeginSec - currentSecond
        endRemainSec = note.EndSec - currentSecond

        lenBySec = self._hitLineY / self._noteDropSec  # 시간별 위치

        beginY = lenBySec * (self._noteDropSec - beginRemainSec)
        endY = lenBySec * (self._noteDropSec - endRemainSec)

        return endY, beginY - endY  # endY가 위에 있음
