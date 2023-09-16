import pygame
import sys

import ui
from . import music

DropSecs = [5, 3, 2, 1.5, 1, 0.5, 0.3, 0.1]
NoteColors = [(255, 255, 0), (0, 255, 0), (0, 0, 255)]
HitLinePos = 90  # 1 ~ 99 중에 선택


class RhythmGame:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        self._Start()

    # 기본 값들을 설정하고 게임 시작
    def _Start(self):
        self._currentSec = 0
        self._dropSecIdx = 4
        self._finishGame = False
        self._lanePressing = dict()
        self._gameStartTick = pygame.time.get_ticks()
        self._sheet = music.SheetMaker().MakeSheet()
        self._laneCnt = self._sheet.GetLaneCnt()

        self._timeTextBox = ui.TextBox(self._screen, self._width * 9 / 10, self._height / 10)
        self._speedTextBox = ui.TextBox(self._screen, self._width / 10, self._height / 10)

        self._Run()

    # 본격적인 게임 시작
    def _Run(self):
        while True:
            self._screen.fill((0, 0, 0))  # 일단 이전 것들 전부 지우고 시작

            dropSec = DropSecs[self._dropSecIdx]
            self._visibleNotes = self._sheet.ExtractVisibleNotes(self._currentSec, dropSec)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 키보드 입력만 처리
                if event.type == pygame.KEYDOWN:
                    self._HandleKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    self._HandleKeyUp(event.key)

            if self._finishGame:
                return  # 게임 끝남

            self._DrawGame()

            pygame.display.flip()  # 위에서 이뤄진 변화들을 한번에 출력

    # 키 입력 처리
    def _HandleKeyDown(self, key):
        if key == pygame.K_ESCAPE:  # esc 키 누름
            self._finishGame = True
        elif key == pygame.K_EQUALS:  # + 키 누름
            self._dropSecIdx = min(self._dropSecIdx + 1, DropSecs.__len__() - 1)
        elif key == pygame.K_MINUS:  # - 키 누름
            self._dropSecIdx = max(self._dropSecIdx - 1, 0)
        elif pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            self._HandleKeyboardDown(laneNum)

    def _HandleKeyUp(self, key):
        if pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            self._HandleKeyboardUp(laneNum)

    # 건반을 누른 것에 대한 처리
    def _HandleKeyboardDown(self, laneNum):
        self._lanePressing[laneNum] = True

    # 건반을 뗀 것에 대한 처리
    def _HandleKeyboardUp(self, laneNum):
        self._lanePressing[laneNum] = False

    # 게임 화면 출력
    def _DrawGame(self):
        for i in range(0, self._laneCnt):
            self._DrawNotes(i)
            self._DrawKeyboardInput(i)

        self._DrawFrame()
        self._PrintText()

    # 게임 틀 그리기
    def _DrawFrame(self):
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
    def _DrawNotes(self, laneNum):
        # 노트 색깔
        noteColorIdx = laneNum % NoteColors.__len__()
        noteColor = NoteColors[noteColorIdx]

        # 노트 너비 위치
        leftX, width = self._CalcLanePosX(laneNum, 0.3)

        # 노트 높이 위치
        currentTick = pygame.time.get_ticks()
        self._currentSec = (currentTick - self._gameStartTick) / 1000

        for note in self._visibleNotes[laneNum]:
            topY, height = self._CalcNotePosY(self._currentSec, note)

            # 각 노트 그리기
            pygame.draw.rect(self._screen, noteColor, (leftX, topY, width, height))

    # 해당 노트 second 맞는 y 위치 찾기
    def _CalcNotePosY(self, currentSec, note):
        beginRemainSec = note.BeginSec - currentSec
        endRemainSec = note.EndSec - currentSec

        hitLineY = (HitLinePos / 100) * self._height
        dropSec = DropSecs[self._dropSecIdx]
        lenBySec = hitLineY / dropSec  # 시간별 위치

        beginY = (dropSec - beginRemainSec) * lenBySec
        endY = (dropSec - endRemainSec) * lenBySec

        return endY, beginY - endY  # endY가 위에 있음

    # 해당 노트 lane 번호에 맞는 x 위치 찾기
    def _CalcLanePosX(self, laneNum, marginRatio):
        x = self._width / 3
        laneWidth = x / self._laneCnt
        beginX = x + laneNum * laneWidth

        leftMargin = laneWidth * (marginRatio / 2)
        width = laneWidth - 2 * leftMargin

        # 선 굵기 때문에 width 살짝 부족하다;;
        width += laneWidth / 30

        return beginX + leftMargin, width

    # 각종 텍스트 출력하기
    def _PrintText(self):
        speed = str(self._dropSecIdx + 1)
        self._speedTextBox.Print("Speed: x" + speed, 20, True, "white")

        currentSec = "{:.1f}".format(self._currentSec)
        self._timeTextBox.Print(currentSec + "s", 20, False, "white")

    # 건반을 누른 것에 대한 표현
    def _DrawKeyboardInput(self, laneNum):
        if laneNum not in self._lanePressing:
            return
        if not self._lanePressing[laneNum]:
            return

        y = self._height
        hitLineY = (HitLinePos / 100) * y
        effectHalfLen = y - hitLineY
        height = 2 * effectHalfLen

        effectStartX, width = self._CalcLanePosX(laneNum, 0.15)

        effectColor = (128, 128, 128)

        pygame.draw.rect(self._screen, effectColor, (effectStartX, hitLineY, width, height))
