import pygame


class TextBox:
    def __init__(self, screen, x, y):
        self._screen = screen
        self._center = (x, y)

        self._rect = None

    def Print(self, text, size, isBold, color, alpha):
        font = pygame.font.SysFont("malgungothic", size, isBold, False)
        surface = font.render(text, True, color)
        surface.set_alpha(alpha)

        self._rect = surface.get_rect(center=self._center)
        self._screen.blit(surface, self._rect)

    # 해당 color 덮어버리기
    def Clear(self, color):
        if self._rect is None:
            return

        pygame.draw.rect(self._screen, color, self._rect)
