import pygame.display

import etc
import ui
from .rhythm_game import *
from .manager.music_manager import *


class MainMenu:
    _TitleColors = ["chocolate1", "darkblue"]
    _TitleChangeSec = 0.5

    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 필수 준비물 (악기, 악보)
        self._musicManager = music_manager()

        # 게임 한판 끝나면, 다시 메뉴로 돌아오면서 다시 시작
        while True:
            self._Start()

    # 메인 메뉴의 시작. 기본 설정만 하고, run!
    def _Start(self):
        # 배경 설정
        self._screen.fill("white")
        pygame.display.update()

        # 타이틀 설정
        self._CreateTitle()

        # 버튼들 설정
        self._buttons = []
        self._CreateButton(self._width / 2, self._height * (4 / 8), "게임 하기", self._StartRhythmGame)
        self._CreateButton(self._width / 2, self._height * (5 / 8), "음악 듣기", self._ListenRhythmGame)
        self._CreateButton(self._width / 2, self._height * (6 / 8), "만든 사람", None)
        self._CreateButton(self._width / 2, self._height * (7 / 8), "나가기", etc.ExitGame)

        self._Run()

    # 실질적인 메뉴 진행. 여기서 게임 한판 종료까지 쭉 진행한다
    def _Run(self):
        while True:
            mousePos = pygame.mouse.get_pos()
            mousePressMove = pygame.mouse.get_pressed()
            mouseLeftPressMove = mousePressMove[0]  # 마우스 누르고 움직일 때

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if self._HandleButtonClick(mousePos):
                        return  # 뭔가 행동 하나 진행. 처음부터 다시 시작하자
                elif event.type == pygame.MOUSEBUTTONDOWN or mouseLeftPressMove:
                    self._HandleButtonPressing(mousePos)
                else:
                    self._HandleButtonHovering(mousePos)

            # 타이틀은 계속 깜빡 깜빡
            self._ChangeTitleColor()

            pygame.display.flip()

    def _CreateTitle(self):
        x = self._width / 2
        y = self._height / 4

        self._titleBox = ui.TextBox(self._screen, x, y)
        self._lastTitleColorIdx = 0
        self._lastTitleColorTick = pygame.time.get_ticks()
        self._PrintTitle()

    # 제목을 반짝 반짝 꾸며줌
    def _ChangeTitleColor(self):
        currentTickTime = pygame.time.get_ticks()
        elapsedSec = (currentTickTime - self._lastTitleColorTick) / 1000
        if elapsedSec < self._TitleChangeSec:
            return

        self._lastTitleColorIdx += 1
        if self._lastTitleColorIdx == self._TitleColors.__len__():
            self._lastTitleColorIdx = 0
        self._PrintTitle()

        self._lastTitleColorTick = currentTickTime

    def _PrintTitle(self):
        color = self._TitleColors[self._lastTitleColorIdx]
        self._titleBox.Print("예찬쌤의 리듬 게임", 100, True, color, 255)

    # 버튼 추가
    def _CreateButton(self, x, y, text, clickFunc):
        button = ui.Button(self._screen, x, y, text, clickFunc)
        self._buttons.append(button)

    # 마우스를 버튼 위에 올렸을 때 처리
    def _HandleButtonHovering(self, mousePos):
        for button in self._buttons:
            button.Hovering(mousePos)

    # 마우스를 누른채 버튼 위에 올렸을 때 처리
    def _HandleButtonPressing(self, mousePos):
        for button in self._buttons:
            button.Pressing(mousePos)

    # 마우스를 클릭 했을 때 처리
    def _HandleButtonClick(self, mousePos):
        for button in self._buttons:
            if button.Click(mousePos):
                return True
            
        return False

    # 게임 시작
    def _StartRhythmGame(self):
        self._rhythmGame(False)

    # 자동 플레이 (음악 듣기)
    def _ListenRhythmGame(self):
        self._rhythmGame(True)

    # 리듬 게임 시작
    def _rhythmGame(self, autoPlay):
        etc.ScreenBlackOut(self._screen)  # 화면 어두워지기
        
        instrument, sheet = self._musicManager.GetCurrentMusic()
        RhythmGame(self._screen, instrument, sheet, autoPlay)
