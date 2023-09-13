import pygame
import sys

from etc.button import Button
from etc.text import TextBox


class MainMenu:
    _TitleColors = ["red", "blue"]
    _TitleChangeSec = 0.5

    def __init__(self, screen):
        self._screen = screen

        # 게임 한판 끝나면, 다시 메뉴로 돌아오면서 다시 시작
        while True:
            self._start()

    # 메인 메뉴의 시작. 기본 설정만 하고, run!
    def _start(self):
        # 배경 설정
        pygame.display.set_caption("main menu")
        self._screen.fill("white")
        pygame.display.update()

        # 타이틀 설정
        width, height = pygame.display.get_surface().get_size()
        self._createTitle(width / 2, height / 5)

        self._run()

    # 실질적인 메뉴 진행. 여기서 게임 한판 종료까지 쭉 진행한다
    def _run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    return

            self._changeTitleColor()

    def _createTitle(self, x, y):
        self.titleBox = TextBox(self._screen, x, y)
        self.lastTitleIdx = 0
        self.lastTickTime = pygame.time.get_ticks()
        self._printTitle()

    # 제목을 반짝 반짝 꾸며줌
    def _changeTitleColor(self):
        currentTickTime = pygame.time.get_ticks()
        elapsedSec = (currentTickTime - self.lastTickTime) / 1000
        if elapsedSec < self._TitleChangeSec:
            return

        self.lastTitleIdx += 1
        if self.lastTitleIdx == self._TitleColors.__len__():
            self.lastTitleIdx = 0
        self._printTitle()

        self.lastTickTime = pygame.time.get_ticks()

    def _printTitle(self):
        color = self._TitleColors[self.lastTitleIdx]
        self.titleBox.Print("둠칫 둠칫 리듬 게임", 30, color)