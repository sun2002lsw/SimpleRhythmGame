import pygame

BUTTON_SIZE = 100


class Button:
    def __init__(self, screen, x, y, text, clickFunc):
        self._screen = screen
        self._x = x
        self._y = y
        self._text = text
        self._clickFunc = clickFunc

        self._setButtonSize(BUTTON_SIZE)
        self._drawDefaultButton()
        self._defaultState = True

    # 마우스를 버튼 위에 올렸을 때
    def Hovering(self, mousePos):
        if not self._isInsideButton(mousePos):
            if not self._defaultState:
                self._drawDefaultButton()
            return

        self._drawActiveButton(30)

    # 마우스를 누른채 버튼 위에 올렸을 때
    def Pressing(self, mousePos):
        if not self._isInsideButton(mousePos):
            if not self._defaultState:
                self._drawDefaultButton()
            return

        self._drawActiveButton(25)

    # 마우스를 클릭 했을 때
    def Click(self, mousePos):
        if not self._isInsideButton(mousePos):
            return

        self._drawActiveButton(35)
        self._clickFunc()

    # 버튼 생성
    def _drawDefaultButton(self):
        self._defaultState = True
        self._drawButton(30, "black", (0, 128, 0), False)

    def _drawActiveButton(self, textSize):
        self._defaultState = False
        self._drawButton(textSize, "white", (0, 128, 0), True)

    def _drawFadeoutButton(self):
        self._defaultState = False
        self._drawButton(35, "white", (0, 0, 0), True)

    def _drawButton(self, textSize, textColor, backgroundColor, isBold):
        font = pygame.font.SysFont("malgungothic", textSize, isBold, False)
        surface = font.render(self._text, True, textColor)
        textRect = surface.get_rect()
        textRect.center = self._buttonRect.center

        pygame.draw.rect(self._screen, backgroundColor, self._buttonRect)
        self._screen.blit(surface, textRect)

        pygame.display.update(self._buttonRect)

    # x, y 좌표가 버튼에 들어왔는지 확인
    def _isInsideButton(self, mousePos):
        x = mousePos[0]
        y = mousePos[1]

        if x < self._buttonRect.left or self._buttonRect.right < x:
            return False
        if y < self._buttonRect.top or self._buttonRect.bottom < y:
            return False

        return True

    def _setButtonSize(self, buttonSize):
        left = self._x - buttonSize
        top = self._y - buttonSize / 3
        width = buttonSize * 2
        height = width / 3

        self._buttonRect = pygame.Rect(left, top, width, height)