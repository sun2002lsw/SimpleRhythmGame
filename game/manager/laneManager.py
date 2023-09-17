import pygame


class LaneManager:
    def __init__(self, screen, laneLeftX, laneWidth, hitLineY, notes, noteColor, noteDropSec):
        self._screen = screen
        self._laneLeftX = laneLeftX
        self._laneWidth = laneWidth
        self._hitLineY = hitLineY
        self._notes = notes
        self._noteColor = noteColor
        self._noteDropSec = noteDropSec
        self._isPressing = False

        # 노트의 x 위치와 너비
        leftMargin = self._laneWidth * 0.15
        self._noteWidth = self._laneWidth - 2 * leftMargin
        self._noteWidth += self._laneWidth / 30  # 선 굵기 때문에 width 살짝 부족하다;;
        self._noteLeftX = self._laneLeftX + leftMargin

    def SetNoteDropSec(self, noteDropSec):
        self._noteDropSec = noteDropSec

    def HandleKeyDown(self):
        self._isPressing = True

    def HandleKeyUp(self):
        self._isPressing = False

    # 해당 라인의 상황 그리기
    def Draw(self, currentSecond):
        if len(self._notes) == 0:
            return

        self._DelOutOfScreenNote(currentSecond)
        self._DrawNotes(currentSecond)
        self._DrawInput()

    # 화면 밖으로 사라진 노트 지우기
    def _DelOutOfScreenNote(self, currentSecond):
        outOfScreenSec = currentSecond - self._noteDropSec

        if self._notes[0].EndSec < outOfScreenSec:
            self._notes.pop(0)

    # 각 노트들 그리기
    def _DrawNotes(self, currentSecond):
        inTheScreenSec = currentSecond + self._noteDropSec
        visibleNotes = [note for note in self._notes if note.BeginSec < inTheScreenSec]

        for note in visibleNotes:
            topY, height = self._CalcNotePosY(currentSecond, note)
            noteRect = (self._noteLeftX, topY, self._noteWidth, height)
            pygame.draw.rect(self._screen, self._noteColor, noteRect)

    # 해당 노트 second 맞는 y 위치와 길이 찾기
    def _CalcNotePosY(self, currentSecond, note):
        beginRemainSec = note.BeginSec - currentSecond
        endRemainSec = note.EndSec - currentSecond

        lenBySec = self._hitLineY / self._noteDropSec  # 시간별 위치

        beginY = lenBySec * (self._noteDropSec - beginRemainSec)
        endY = lenBySec * (self._noteDropSec - endRemainSec)

        return endY, beginY - endY  # endY가 위에 있음

    # 키를 눌렀을 때 효과 그리기
    def _DrawInput(self):
        if self._isPressing:
            color = (128, 128, 128)
            startPos = (self._noteLeftX, self._hitLineY)
            endPos = (self._noteLeftX + self._noteWidth, self._hitLineY)
            width = 20

            pygame.draw.line(self._screen, color, startPos, endPos, width)
