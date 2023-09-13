import pygame

from etc.button import Button
from etc.func import ExitGame
from etc.text import TextBox


# 더미 함수
def _dummy():
    pass


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
        self._screen.fill("white")
        pygame.display.update()

        # 타이틀 설정
        width, height = pygame.display.get_surface().get_size()
        self._createTitle(width / 2, height / 4)

        # 버튼들 설정
        self._buttons = []
        self._createButton(width / 2, height * (3 / 6), "게임 시작", _dummy)
        self._createButton(width / 2, height * (4 / 6), "자동 사냥", _dummy)
        self._createButton(width / 2, height * (5 / 6), "나가기", ExitGame)

        self._run()

    # 실질적인 메뉴 진행. 여기서 게임 한판 종료까지 쭉 진행한다
    def _run(self):
        while True:
            mousePos = pygame.mouse.get_pos()
            mousePressMove = pygame.mouse.get_pressed()
            mouseLeftPressMove = mousePressMove[0]  # 마우스 누르고 움직일 때

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    self._handleButtonClick(mousePos)
                elif event.type == pygame.MOUSEBUTTONDOWN or mouseLeftPressMove:
                    self._handleButtonPressing(mousePos)
                else:
                    self._handleButtonHovering(mousePos)

            # 타이틀은 계속 깜빡 깜빡
            self._changeTitleColor()

    def _createTitle(self, x, y):
        self.titleBox = TextBox(self._screen, x, y)
        self._lastTitleColorIdx = 0
        self._lastTitleColorTick = pygame.time.get_ticks()
        self._printTitle()

    # 제목을 반짝 반짝 꾸며줌
    def _changeTitleColor(self):
        currentTickTime = pygame.time.get_ticks()
        elapsedSec = (currentTickTime - self._lastTitleColorTick) / 1000
        if elapsedSec < self._TitleChangeSec:
            return

        self._lastTitleColorIdx += 1
        if self._lastTitleColorIdx == self._TitleColors.__len__():
            self._lastTitleColorIdx = 0
        self._printTitle()

        self._lastTitleColorTick = currentTickTime

    def _printTitle(self):
        color = self._TitleColors[self._lastTitleColorIdx]
        self.titleBox.Print("예찬쌤의 리듬 게임", 100, color)

    # 버튼 추가
    def _createButton(self, x, y, text, clickFunc):
        button = Button(self._screen, x, y, text, clickFunc)
        self._buttons.append(button)

    # 마우스를 버튼 위에 올렸을 때 처리
    def _handleButtonHovering(self, mousePos):
        for button in self._buttons:
            button.Hovering(mousePos)

    # 마우스를 누른채 버튼 위에 올렸을 때 처리
    def _handleButtonPressing(self, mousePos):
        for button in self._buttons:
            button.Pressing(mousePos)

    # 마우스를 클릭 했을 때 처리
    def _handleButtonClick(self, mousePos):
        for button in self._buttons:
            button.Click(mousePos)
