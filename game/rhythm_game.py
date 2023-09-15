import pygame
import sys

from . import music

DropSecs = [5, 3, 2, 1.5, 1, 0.5, 0.3, 0.1]
NoteColors = [(255, 255, 0), (0, 255, 0), (0, 0, 255)]
HitLinePos = 80  # 1 ~ 99 중에 선택


class RhythmGame:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 기본 빈 값 설정
        self._sheet = music.Sheet()
        self._laneCnt = 0
        self._dropSecIdx = 4
        self._gameStartTick = 0

        self._start()

    # 기본 값들을 설정하고 게임 시작
    def _start(self):
        self._createSheet()
        self._laneCnt = self._sheet.GetLaneCnt()

        self._run()

    # 본격적인 게임 시작
    def _run(self):
        self._gameStartTick = pygame.time.get_ticks()

        while True:
            self._drawGame()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # 게임 화면 출력
    def _drawGame(self):
        self._screen.fill((0, 0, 0))

        for i in range(0, self._laneCnt):
            self._drawNotes(i)
        self._drawFrame()

        pygame.display.flip()

    # 게임 틀 그리기
    def _drawFrame(self):
        x = self._width / 3
        y = self._height

        # 줄 긋는 순서 중요!
        for i in range(1, self._laneCnt):
            laneX = x + i * (x / self._laneCnt)
            pygame.draw.line(self._screen, "white", (laneX, 0), (laneX, y), 1)

        hitLineY = (HitLinePos / 100) * y
        pygame.draw.line(self._screen, "red", (x, hitLineY), (2 * x, hitLineY), 10)

        pygame.draw.line(self._screen, "white", (x, 0), (x, y), 5)
        pygame.draw.line(self._screen, "white", (2 * x, 0), (2 * x, y), 5)

    # 떨어지는 노트 그리기
    def _drawNotes(self, laneNum):
        # 노트 색깔
        noteColorIdx = laneNum % NoteColors.__len__()
        noteColor = NoteColors[noteColorIdx]

        # 노트 너비 위치
        leftX, width = self._calcNotePosX(laneNum)

        # 노트 높이 위치
        currentTick = pygame.time.get_ticks()
        currentSec = (currentTick - self._gameStartTick) / 1000
        dropSec = DropSecs[self._dropSecIdx]

        drawableNotes = self._sheet.ExtractDrawableNotes(laneNum, currentSec, dropSec)
        for note in drawableNotes:
            topY, height = self._calcNotePosY(currentSec, note)

            # 각 노트 그리기
            pygame.draw.rect(self._screen, noteColor, (leftX, topY, width, height))

    # 해당 노트 second 맞는 y 위치 찾기
    def _calcNotePosY(self, currentSec, note):
        beginRemainSec = note.BeginSec - currentSec
        endRemainSec = note.EndSec - currentSec

        hitLineY = (HitLinePos / 100) * self._height
        dropSec = DropSecs[self._dropSecIdx]
        lenBySec = hitLineY / dropSec  # 시간별 위치

        beginY = (dropSec - beginRemainSec) * lenBySec
        endY = (dropSec - endRemainSec) * lenBySec

        return endY, beginY - endY  # endY가 위에 있음

    # 해당 노트 lane 번호에 맞는 x 위치 찾기
    def _calcNotePosX(self, laneNum):
        x = self._width / 3
        laneWidth = x / self._laneCnt
        beginX = x + laneNum * laneWidth

        laneMargin = laneWidth / 8
        noteWidth = laneWidth - 2 * laneMargin

        return beginX + laneMargin, noteWidth

    # 악보 만들기 (이거 다른 모듈로 빼야겠지?)
    def _createSheet(self):
        initNote = music.Note(0, 0)

        self._sheet.AddNote(0, initNote)
        self._sheet.AddNote(1, initNote)
        self._sheet.AddNote(2, initNote)
        self._sheet.AddNote(3, initNote)

        note1 = music.Note(1, 3)
        self._sheet.AddNote(0, note1)
        self._sheet.AddNote(3, note1)

        note2 = music.Note(2, 1)
        self._sheet.AddNote(1, note2)

        note3 = music.Note(4, 3)
        self._sheet.AddNote(3, note3)
