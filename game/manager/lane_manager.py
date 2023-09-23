from .effect_manager import *
from ..music.lane_note import LaneNoteState
from .score_manager import ComboState


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
        self._comboState = ComboState.NoChange
        self._lastMeltingComboSec = 0

        # 펑펑 화려한 이펙트 관리자
        self._effectManager = EffectManager(screen, laneLeftX, laneWidth, hitLineY)

        # 노트의 x 위치와 너비
        leftMargin = self._laneWidth * 0.1
        self._noteWidth = self._laneWidth - 2 * leftMargin
        self._noteWidth += self._laneWidth / 30  # 선 굵기 때문에 width 살짝 부족하다;;
        self._noteLeftX = self._laneLeftX + leftMargin

    # 놓치는 노트 확인
    def CheckMiss(self, currentSecond):
        for note in self._notes:
            if note.BeginSec > currentSecond:
                break  # 여기 i 부터는 아직 확인할 필요 없는 노트

            if note.State == LaneNoteState.Drop:
                if currentSecond - 0.2 < note.BeginSec < currentSecond:
                    self._effectManager.StartOnce(EffectType.Danger)
                if note.BeginSec < currentSecond - 0.2:
                    self._SetNoteMiss(note)

            if note.State == LaneNoteState.Hit:
                if note.EndSec < currentSecond - 0.2:
                    self._SetNoteMiss(note)
                    self._effectManager.Stop(EffectType.Melting)

    def _SetNoteMiss(self, note):
        note.State = LaneNoteState.Miss

        self._comboState = ComboState.Miss
        self._effectManager.Start(EffectType.Miss)

    # 노트 hit 해서 쭉 녹이는 과정 진행
    def ProcessMelting(self, currentSecond):
        if not self._isPressing:
            return

        hitNote = None
        for note in self._notes:
            if note.State == LaneNoteState.Hit:
                hitNote = note
                break
        if hitNote is None:
            return

        hitNote.BeginSec = currentSecond
        self._effectManager.StartOnce(EffectType.Melting)
        if self._lastMeltingComboSec + 0.1 < currentSecond:
            self._lastMeltingComboSec = currentSecond
            self._comboState = ComboState.Hit

    # 타이밍 맞춰서 키 누름
    def HandleKeyDown(self, currentSecond):
        self._isPressing = True

        # 놓치지 않은 가장 가까운 노트
        firstDropNote = None
        for note in self._notes:
            if note.State == LaneNoteState.Drop:
                firstDropNote = note
                break
        if firstDropNote is None:
            return

        if firstDropNote.BeginSec > currentSecond + 1:
            return  # 아직 노트 도착까지 한참 남음

        if currentSecond - 0.2 < firstDropNote.BeginSec < currentSecond + 0.2:
            firstDropNote.State = LaneNoteState.Hit  # 타이밍 맞게 맞췄다
            self._comboState = ComboState.Hit
            if currentSecond - 0.1 < firstDropNote.BeginSec < currentSecond + 0.1:
                self._effectManager.Start(EffectType.PerfectHit)
            else:
                self._effectManager.Start(EffectType.GoodHit)
        else:  # 너무 빨리 눌렀다
            self._SetNoteMiss(firstDropNote)

    # 타이밍 맞춰서 키 뗌
    def HandleKeyUp(self, currentSecond):
        self._isPressing = False

        hitNote = None
        hitNoteIdx = None
        for i, note in enumerate(self._notes):
            if note.State == LaneNoteState.Hit:
                hitNote = note
                hitNoteIdx = i
                break
        if hitNote is None:
            return

        self._effectManager.Stop(EffectType.Melting)

        if currentSecond - 0.2 < hitNote.EndSec < currentSecond + 0.2:
            self._notes.pop(hitNoteIdx)  # 노트 하나를 성공적으로 녹여버림
            self._comboState = ComboState.Hit
            self._effectManager.Start(EffectType.Explosion)
            if currentSecond - 0.1 < hitNote.EndSec < currentSecond + 0.1:
                self._effectManager.Start(EffectType.PerfectHit)
            else:
                self._effectManager.Start(EffectType.GoodHit)
        else:  # 너무 빨리 뗐다
            self._SetNoteMiss(hitNote)

    # 노트 떨어지는 속도 변경
    def SetNoteDropSec(self, noteDropSec):
        self._noteDropSec = noteDropSec

    # 현재의 콤보 상태 확인
    def GetComboState(self):
        comboState = self._comboState
        self._comboState = ComboState.NoChange
        return comboState

    # 해당 라인의 상황 그리기
    def Draw(self, currentSecond):
        self._DrawInput()
        self._DrawNotes(currentSecond)
        self._effectManager.Draw()

    # 키를 눌렀을 때 효과 그리기
    def _DrawInput(self):
        if not self._isPressing:
            return
        
        # 히트 중에는 출력 안 함
        hitNote = None
        for note in self._notes:
            if note.State == LaneNoteState.Hit:
                hitNote = note
                break
        if hitNote is not None:
            return

        for i in range(0, 200):
            rgb = int(255 - 1.25 * i)
            color = (rgb, rgb, rgb)

            y = self._laneBottomY - i
            startPos = (self._noteLeftX, y)
            endPos = (self._noteLeftX + self._noteWidth - 2, y)

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
