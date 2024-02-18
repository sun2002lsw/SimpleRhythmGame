import math

import pygame
import sys

import etc
from ui import TextBox
from .manager import LaneManager
from .manager import ScoreManager

DropSecs = [5, 3, 2, 1.5, 1, 0.5, 0.3, 0.1]
NoteColors = [(185, 235, 255), (255, 255, 194), (81, 35, 200)]
HitLinePos = 90  # 1 ~ 99 중에 선택


class RhythmGame:
    def __init__(self, screen, instrument, sheet, autoPlay):
        self._screen = screen
        self._instrument = instrument
        self._sheet = sheet
        self._autoPlay = autoPlay

        width, height = pygame.display.get_surface().get_size()
        self._screenWidth = width
        self._screenHeight = height
        
        # 게임 틀 관련 설정
        self._frameLeftX = self._screenWidth / 3  # 게임 화면은 전체 화면의 1/3로 고정
        self._hitLineY = height * HitLinePos / 100  # 히트 라인도 특정 위치 고정

        # 악기 그림 관련 설정 (그림이 없을 수도 있음)
        image = self._instrument.GetImage()
        if image is not None:
            size = (self._screenWidth / 2, height * (100 - HitLinePos) / 100)
            self._instrumentImage = pygame.transform.scale(image, size)
            rect = self._instrumentImage.get_rect()
            self._instrumentImageRect = rect.move(self._screenWidth / 4, self._hitLineY)
        else:
            self._instrumentImage = None

        # 게임 시작
        self._Start()

    # 기본 값들을 설정하고 게임 시작
    def _Start(self):
        self._dropSecIdx = 4
        self._finishGame = False
        self._finishSec = self._sheet.GetFinishSec()

        self._instrument.Ready()
        self._sheet.Ready()

        # 양 옆의 각종 정보 표시 공간
        self._timeTextBox = TextBox(self._screen, self._screenWidth * 9 / 10, self._screenHeight / 10)
        self._speedTextBox = TextBox(self._screen, self._screenWidth / 10, self._screenHeight / 10)
        self._pitchTextBox = TextBox(self._screen, self._screenWidth / 6, self._screenHeight / 2)
        self._scoreManager = ScoreManager(self._screen, self._screenWidth, self._screenHeight)

        # 중앙의 노트 떨어지는 공간
        self._laneNotes = self._sheet.GetLaneNotesForInstrument(self._instrument)
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
                              notes, noteColor, noteDropSec, self._autoPlay)

            self._laneManagers[laneNum] = mgr

    # 본격적인 게임 시작
    def _Run(self):
        while True:
            self._currentSec = (pygame.time.get_ticks() - self._gameStartTick) / 1000
            pitch = self._sheet.GetPitchByCurrentSec(self._currentSec)

            for laneManager in self._laneManagers.values():
                laneManager.CheckMiss(self._currentSec)
                laneManager.ProcessMelting(self._currentSec)
                comboState = laneManager.GetComboState()

                self._scoreManager.AddComboState(comboState, pitch)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # 게임 키보드 입력 처리
                if event.type == pygame.KEYDOWN:
                    self._HandleKeyDown(event.key)
                elif event.type == pygame.KEYUP:
                    self._HandleKeyUp(event.key)

                # esc 키 누름
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._finishGame = True

            # 게임 화면에 그리기
            self._DrawGame()

            # 자동 플레이인 경우 알아서 소리 재생
            if self._autoPlay:
                startPitch = self._sheet.GetStartPitchByCurrentSec(self._currentSec)
                self._instrument.PlayPitchSound(startPitch)

            # 게임 플레이 완료
            if self._finishGame or self._finishSec < self._currentSec:
                etc.ScreenBlackOut(self._screen)
                break

        # 플레이 종료에 따른 점수 표기
        self._scoreManager.DrawResult()

        # 아무 키나 누를 때까지 대기
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    etc.ScreenWhiteOut(self._screen)
                    return

    # 키 입력 처리
    def _HandleKeyDown(self, key):
        if key == pygame.K_EQUALS:  # + 키 누름
            self._dropSecIdx = min(self._dropSecIdx + 1, DropSecs.__len__() - 1)
            self._ChangeNoteDropSec()
        elif key == pygame.K_MINUS:  # - 키 누름
            self._dropSecIdx = max(self._dropSecIdx - 1, 0)
            self._ChangeNoteDropSec()
        elif not self._autoPlay and pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            if laneNum in self._laneManagers:
                self._laneManagers[laneNum].HandleKeyDown(self._currentSec)
            self._instrument.PlayKeyDownSound(laneNum)

    def _HandleKeyUp(self, key):
        if self._autoPlay:
            return

        if pygame.K_0 <= key <= pygame.K_9:
            laneNum = key - pygame.K_0
            if laneNum in self._laneManagers:
                self._laneManagers[laneNum].HandleKeyUp(self._currentSec)
            self._instrument.PlayKeyUpSound(laneNum)

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
        self._DrawInstrumentImage()
        self._PrintText()
        self._scoreManager.Draw()

        pygame.display.flip()

    # 게임 틀 그리기 (줄 긋는 순서 중요!)
    def _DrawFrame(self):
        x = self._frameLeftX
        y = self._screenHeight

        # 노트 라인 구분선
        laneWidth = x / self._laneCnt
        for i in range(1, self._laneCnt):
            laneX = x + i * laneWidth
            startPos = (laneX, 0)
            endPos = (laneX, y)

            lineColor = "white"
            lineWidth = 1
            if self._laneCnt > 1 and i == math.ceil(self._laneCnt / 2):
                lineColor = "red"
                lineWidth = 3

            pygame.draw.line(self._screen, lineColor, startPos, endPos, lineWidth)

        # 히트 라인
        startPos = (x, self._hitLineY)
        endPos = (2 * x, self._hitLineY)
        pygame.draw.line(self._screen, "red", startPos, endPos, 10)

        # 게임 테두리
        pygame.draw.line(self._screen, "white", (x, 0), (x, y), 5)
        pygame.draw.line(self._screen, "white", (2 * x, 0), (2 * x, y), 5)

    # 악기 그림 그리기
    def _DrawInstrumentImage(self):
        if self._instrumentImage is None:
            return

        self._screen.blit(self._instrumentImage, self._instrumentImageRect)

    # 각종 텍스트 출력하기
    def _PrintText(self):
        speed = str(self._dropSecIdx + 1)
        self._speedTextBox.Print("Speed: x" + speed, 20, True, "white", 255)

        currentSecStr = "{:.1f}".format(self._currentSec)
        self._timeTextBox.Print(currentSecStr + "s", 20, False, "white", 255)

        pitch = self._sheet.GetPitchByCurrentSec(self._currentSec)
        if pitch != "쉼표":
            self._pitchTextBox.Print(pitch, 75, True, "yellow", 255)
