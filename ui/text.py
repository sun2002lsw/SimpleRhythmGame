import pygame


class TextBox:
    def __init__(self, screen, x, y):
        self._screen = screen
        self._center = (x, y)

    def Print(self, text, size, isBold, color):
        font = pygame.font.SysFont("malgungothic", size, isBold, False)
        surface = font.render(text, True, color)
        rect = surface.get_rect(center=self._center)

        self._screen.blit(surface, rect)
        pygame.display.update(rect)
