import pygame
import sys

from ui import TextBox
from .music import Sheet
from .manager import LaneManager
from .manager import ScoreManager

DropSecs = [5, 3, 2, 1.5, 1, 0.5, 0.3, 0.1]
NoteColors = [(255, 255, 0), (0, 255, 0), (0, 0, 255)]
HitLinePos = 90  # 1 ~ 99 중에 선택


class RhythmGame:
    def __init__(self, screen, instrument):
        self._screen = screen
        self._instrument = instrument

        width, height = pygame.display.get_surface().get_size()
        self._screenWidth = width
        self._screenHeight = height
        
        self._frameLeftX = self._screenWidth / 3  # 게임 화면은 전체 화면의 1/3로 고정
        self._hitLineY = height * HitLinePos / 100  # 히트 라인도 특정 위치 고정

        self._Start()

    # 기본 값들을 설정하고 게임 시작
    def _Start(self):
        self._dropSecIdx = 4
        self._finishGame = False

        self._timeTextBox = TextBox(self._screen, self._screenWidth * 9 / 10, self._screenHeight / 10)
        self._speedTextBox = TextBox(self._screen, self._screenWidth / 10, self._screenHeight / 10)
        self._scoreManager = ScoreManager(self._screen, self._screenWidth, self._screenHeight)

        self._laneNotes = Sheet().GetLaneNotes()
        self._laneCnt = self._instrument.GetLaneCnt()
        self._InitLaneManager()

        self._gameStartTick = pygame.time.get_ticks()
        self._Run()

    # 각 라인의 매니저 설정
    def _InitLaneManager(self):
        self._laneManagers = dict()

        laneWidth = self._frameLeftX / self._laneCnt
        noteDropSec = DropSecs[self._dropSecIdx]
        
        for laneNum in range(0, self._laneCnt):
            laneLeftX = self._frameLeftX + laneNum * laneWidth
            notes = self._laneNotes[laneNum]
            noteColorIdx = laneNum % NoteColors.__len__()
            noteColor = NoteColors[noteColorIdx]

            mgr = LaneManager(self._screen,
                              laneLeftX, laneWidth, self._screenHeight, self._hitLineY,
                              notes, noteColor, noteDropSec)

            self._laneManagers[laneNum] = mgr

    # 본격적인 게임 시작
    def _Run(self):
        while True:
            self._currentSec = (pygame.time.get_ticks() - self._gameStartTick) / 1000

            for laneManager in self._laneManagers.values():
                laneManager.CheckMiss(self._currentSec)
                laneManager.ProcessMelting(self._currentSec)
                comboState = laneManager.GetComboState()
                self._scoreManager.AddComboState(comboState)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 키보드 입력만 처리
                if event.type == pygame.KEYDOWN:
                    self._HandleKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    self._HandleKeyUp(event.key)

            self._DrawGame()
            if self._finishGame:
                return

    # 키 입력 처리
    def _HandleKeyDown(self, key):
        if key == pygame.K_ESCAPE:  # esc 키 누름
            self._finishGame = True
        elif key == pygame.K_EQUALS:  # + 키 누름
            self._dropSecIdx = min(self._dropSecIdx + 1, DropSecs.__len__() - 1)
            self._ChangeNoteDropSec()
        elif key == pygame.K_MINUS:  # - 키 누름
            self._dropSecIdx = max(self._dropSecIdx - 1, 0)
            self._ChangeNoteDropSec()
        elif pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            if laneNum in self._laneManagers:
                self._laneManagers[laneNum].HandleKeyDown(self._currentSec)

    def _HandleKeyUp(self, key):
        if pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            if laneNum in self._laneManagers:
                self._laneManagers[laneNum].HandleKeyUp(self._currentSec)

    def _ChangeNoteDropSec(self):
        noteDropSec = DropSecs[self._dropSecIdx]

        for laneManager in self._laneManagers.values():
            laneManager.SetNoteDropSec(noteDropSec)

    # 게임 화면 출력
    def _DrawGame(self):
        self._screen.fill((0, 0, 0))

        for laneManager in self._laneManagers.values():
            laneManager.Draw(self._currentSec)

        self._DrawFrame()
        self._PrintText()
        self._scoreManager.Draw()

        pygame.display.flip()

    # 게임 틀 그리기 (줄 긋는 순서 중요!)
    def _DrawFrame(self):
        x = self._frameLeftX
        y = self._screenHeight

        # 노트 라인 구분선
        """
        laneWidth = x / self._laneCnt
        for i in range(1, self._laneCnt):
            laneX = x + i * laneWidth
            startPos = (laneX, 0)
            endPos = (laneX, y)

            pygame.draw.line(self._screen, "white", startPos, endPos, 1)
        """

        # 히트 라인
        startPos = (x, self._hitLineY)
        endPos = (2 * x, self._hitLineY)
        pygame.draw.line(self._screen, "red", startPos, endPos, 10)

        # 게임 테두리
        pygame.draw.line(self._screen, "white", (x, 0), (x, y), 5)
        pygame.draw.line(self._screen, "white", (2 * x, 0), (2 * x, y), 5)

    # 각종 텍스트 출력하기
    def _PrintText(self):
        speed = str(self._dropSecIdx + 1)
        self._speedTextBox.Print("Speed: x" + speed, 20, True, "white", 255)

        currentSec = "{:.1f}".format(self._currentSec)
        self._timeTextBox.Print(currentSec + "s", 20, False, "white", 255)
