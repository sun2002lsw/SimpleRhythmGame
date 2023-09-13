import pygame

BUTTON_SIZE = 100
Width = BUTTON_SIZE * 2
Height = Width / 3


class Button:
	def __init__(self, screen, x, y, text):
		self._screen = screen
		self._buttonRect = pygame.Rect(x - BUTTON_SIZE, y - BUTTON_SIZE / 3, Width, Height)
		self._text = text

		# 글자 만들기
		font = pygame.font.SysFont("malgungothic", 30, False, False)
		surface = font.render(text, True, "black")

		textRect = surface.get_rect()
		textRect.center = self._buttonRect.center
		
		# 버튼 그리기
		pygame.draw.rect(screen, (0, 128, 0), self._buttonRect)
		self._screen.blit(surface, textRect)
		pygame.display.update(self._buttonRect)
