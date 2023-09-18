import pygame

from .effect import Effect


class DangerEffect(Effect):
    def _DrawEffect(self, effectSec):
        if effectSec >= 0.2:
            return True

        for i in range(1, int(effectSec * 50)):
            color = (255 - 25 * i, 0, 0)

            startPos = (self._laneLeftX, self._hitLineY + i)
            endPos = (self._laneLeftX + self._laneWidth - 1, self._hitLineY + i)
            pygame.draw.line(self._screen, color, startPos, endPos)

            startPos = (self._laneLeftX, self._hitLineY - i)
            endPos = (self._laneLeftX + self._laneWidth - 1, self._hitLineY - i)
            pygame.draw.line(self._screen, color, startPos, endPos)

        return False
