import pygame
from enum import Enum, auto

from ui import TextBox


class EffectType(Enum):
    Danger = auto()  # 노트가 히트라인을 지나친 상황
    Miss = auto()  # 노트가 완전히 지나쳐서 놓친 상황
    GoodHit = auto()  # 타이밍 맞게 눌러서 맞춘 상황
    PerfectHit = auto()  # 타이밍 맞게 눌러서 맞춘 상황
    Melting = auto()  # 맞추고 꾹 눌러서 녹이는 상황
    Explosion = auto()  # 맞추고 꾹 눌러서 녹이는 상황


class Effect:
    def __init__(self, screen, laneLeftX, laneWidth, hitLineY):
        self._screen = screen
        self._laneLeftX = laneLeftX
        self._laneWidth = laneWidth
        self._laneCenterX = laneLeftX + laneWidth / 2
        self._hitLineY = hitLineY
        self._startTick = 0

    def StartOnce(self):
        if self._startTick > 0:
            return  # 이미 시작함

        self._startTick = pygame.time.get_ticks()

    def Start(self):
        self._startTick = pygame.time.get_ticks()

    def Stop(self):
        self._startTick = 0

    def Draw(self):
        if self._startTick == 0:
            return  # 그릴게 없음

        effectSec = (pygame.time.get_ticks() - self._startTick) / 1000
        if self._DrawEffect(effectSec):
            self._startTick = 0  # 이펙트 종료

    # hitLine 위에서 팝업되는 글자 효가
    def _DrawPopupText(self, effectSec, text, color):
        if effectSec > 1:
            return True

        x = self._laneCenterX
        y = self._hitLineY - 25 - 75 * effectSec

        textBox = TextBox(self._screen, x, y)
        size = int(self._laneWidth / 4)
        alpha = 255 - int(effectSec * 250)

        size = min(size, 50)
        textBox.Print(text, size, True, color, alpha)

        return False

    def _DrawPopCircle(self, effectSec, interval, width):
        if effectSec > interval:
            return True

        x = self._laneCenterX
        y = self._hitLineY
        radius = (1 + effectSec / interval) * self._laneWidth / 4  # 절반 크기 먹고 시작

        pygame.draw.circle(self._screen, "white", (x, y), radius, width)
        return False

    # 각 상속 객체에서 구현해야 할 세부 이펙트
    def _DrawEffect(self, effectSec):
        pass
