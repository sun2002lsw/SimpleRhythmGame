import sys
import pygame

FADE_OUT_DURATION = 2


# black, white에 대한 처리가 각각 다르다
class ScreenBlackOut:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._surface = pygame.Surface((width, height))
        self._surface.fill((0, 0, 0))

        self._fadeStartTick = pygame.time.get_ticks()
        self._lastFadeSec = 0
        self._Run()

    def _Run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            fadeSec = (pygame.time.get_ticks() - self._fadeStartTick) / 1000
            if fadeSec > FADE_OUT_DURATION:
                return
            if fadeSec - self._lastFadeSec < FADE_OUT_DURATION / 300:
                continue

            self._surface.set_alpha(1)
            self._screen.blit(self._surface, (0, 0))
            pygame.display.flip()

            self._lastFadeSec = fadeSec


class ScreenWhiteOut:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._surface = pygame.Surface((width, height))
        self._surface.fill((255, 255, 255))

        self._fadeStartTick = pygame.time.get_ticks()
        self._lastFadeSec = 0
        self._Run()

    def _Run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            fadeSec = (pygame.time.get_ticks() - self._fadeStartTick) / 1000
            if fadeSec > FADE_OUT_DURATION:
                return
            if fadeSec - self._lastFadeSec < FADE_OUT_DURATION / 300:
                continue

            alpha = int(fadeSec / FADE_OUT_DURATION * 10)
            self._surface.set_alpha(alpha)
            self._screen.blit(self._surface, (0, 0))
            pygame.display.flip()

            self._lastFadeSec = fadeSec
