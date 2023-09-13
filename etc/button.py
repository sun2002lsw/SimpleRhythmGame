import pygame

BUTTON_SIZE = 100
Width = BUTTON_SIZE * 2
Height = Width / 3


class Button:
	def __init__(self, screen, x, y, text):
		self._screen = screen
		self._buttonRect = pygame.Rect(x - BUTTON_SIZE, y - BUTTON_SIZE / 3, Width, Height)
		self._text = text
		self._defaultState = True

		# 기본 글자로 버튼 만들기
		self._drawDefaultButton()

	# 마우스를 버튼 위에 올렸을 때
	def Hovering(self, mousePos):
		if not self._isInsideButton(mousePos):
			if not self._defaultState:
				self._drawDefaultButton()
			return

		# 굵고 흰 글자로 버튼 바꾸기
		font = pygame.font.SysFont("malgungothic", 30, True, False)
		surface = font.render(self._text, True, "white")
		self._drawButton(surface)
		self._defaultState = False

	# 마우스를 누른채 버튼 위에 올렸을 때
	def Pressing(self, mousePos):
		if not self._isInsideButton(mousePos):
			if not self._defaultState:
				self._drawDefaultButton()
			return

		# 굵고 흰 글자의 눌림 표현
		font = pygame.font.SysFont("malgungothic", 25, True, False)
		surface = font.render(self._text, True, "white")
		self._drawButton(surface)
		self._defaultState = False

	# 기본 상태의 버튼을 생성
	def _drawDefaultButton(self):
		font = pygame.font.SysFont("malgungothic", 30, False, False)
		surface = font.render(self._text, True, "black")
		self._drawButton(surface)

	# 주어진 surface 버튼을 생성
	def _drawButton(self, surface):
		textRect = surface.get_rect()
		textRect.center = self._buttonRect.center

		pygame.draw.rect(self._screen, (0, 128, 0), self._buttonRect)
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
