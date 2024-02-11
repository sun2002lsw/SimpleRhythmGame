import pygame.display
from time import sleep

import ui
from .rhythm_game import *
from .manager.music_manager import *


class MainMenu:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 필수 준비물 (악기, 악보)
        self._musicManager = music_manager()

        # 게임 한판 끝나면, 다시 메뉴로 돌아오면서 다시 시작
        while True:
            self._instrumentSelected = False
            self._gameModeSelected = False
            self._sheetSelected = False
            
            self._start()

    # 메인 메뉴에서 순서대로 선택을 진행
    def _start(self):
        self._ClearScreenWithTitle()
        sleep(0.5)

        if self._instrumentSelected is False:
            self._startInstrumentSelection()
            return
        
        if self._gameModeSelected is False:
            self._startGameModeSelection()
            return
            
        if self._sheetSelected is False:
            self._startSheetSelection()
            return

        self._startGame()

    # 흰 바탕에 제목만 그리기
    def _ClearScreenWithTitle(self):
        self._screen.fill("white")

        x = self._width / 2
        y = self._height / 4
        titleImg = pygame.image.load("./game/main_menu_title.png")
        titleImg = pygame.transform.scale(titleImg, (x, y))

        rect = titleImg.get_rect()
        x -= titleImg.get_width() / 2
        y -= titleImg.get_height() / 2
        rect = rect.move((x, y))

        self._screen.blit(titleImg, rect)
        pygame.display.flip()

    # 악기 선택 과정
    def _startInstrumentSelection(self):
        x = self._width * (1 / 2)
        y = self._height * (1 / 2)
        guideBox = ui.TextBox(self._screen, x, y)
        guideBox.Print("악기를 선택하세요", 50, True, "orange", 255)

        x = self._width * (3 / 8)
        y = self._height * (5 / 8)
        leftArrowBox = ui.TextBox(self._screen, x, y)
        leftArrowBox.Print("◀", 50, True, "black", 255)

        x = self._width * (5 / 8)
        y = self._height * (5 / 8)
        rightArrowBox = ui.TextBox(self._screen, x, y)
        rightArrowBox.Print("▶", 50, True, "black", 255)

        x = self._width * (1 / 2)
        y = self._height * (5 / 8)
        instrumentBox = ui.TextBox(self._screen, x, y)
        curInstrument, _ = self._musicManager.GetCurrentMusic()
        instrumentBox.Print(curInstrument.Name, 50, True, "black", 255)

        # 키보드로 악기 선택하기
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = event.key

                    # 나가기 버튼
                    if key is pygame.K_ESCAPE:
                        return

                    # 악기 바꾸기 버튼
                    if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                        instrumentBox.Clear("white")

                        idxChange = (key - pygame.K_RIGHT) * 2 - 1
                        idxChange = -idxChange  # 이렇게 하면 왼쪽은 -1, 오른쪽은 +1
                        self._musicManager.ChangeInstrument(idxChange)
                        self._musicManager.ChangeInstrumentSound()

                        curInstrument, _ = self._musicManager.GetCurrentMusic()
                        instrumentBox.Print(curInstrument.Name, 50, True, "black", 255)

                    # 악기 선택 버튼
                    if key is pygame.K_RETURN:
                        self._instrumentSelected = True
                        self._musicManager.SelectInstrumentSound()
                        return

    # 게임 모드 선택 과정
    def _startGameModeSelection(self):
        pass
    
    # 악보 선택 과정
    def _startSheetSelection(self):
        pass

    # 게임 시작
    def _startGame(self):
        pass
