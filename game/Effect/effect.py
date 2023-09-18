import pygame
from enum import Enum, auto

from ui import TextBox


class EffectType(Enum):
    Danger = auto()  # 노트가 히트라인을 지나친 상황
    Miss = auto()  # 노트가 완전히 지나쳐서 놓친 상황
    GoodHit = auto()  # 타이밍 맞게 눌러서 맞춘 상황
    PerfectHit = auto()  # 타이밍 맞게 눌러서 맞춘 상황
    Melting = auto()  # 맞추고 꾹 눌러서 녹이는 상황


class Effect:
    def __init__(self, screen, laneLeftX, laneWidth, hitLineY):
        self._screen = screen
        self._laneLeftX = laneLeftX
        self._laneWidth = laneWidth
        self._hitLineY = hitLineY
        self._startTick = 0

    def Start(self):
        if self._startTick > 0:
            return  # 이미 시작함

        self._startTick = pygame.time.get_ticks()

    def Draw(self):
        if self._startTick == 0:
            return  # 그릴게 없음

        effectSec = (pygame.time.get_ticks() - self._startTick) / 1000
        if self._DrawEffect(effectSec):
            self._startTick = 0  # 이펙트 종료

    # hitLine 위에서 팝업되는 글자 효가
    def _DrawPopupText(self, effectSec, text, color):
        if effectSec >= 2:
            return True

        x = self._laneLeftX + self._laneWidth / 2
        y = self._hitLineY - 20 - 50 * effectSec

        textBox = TextBox(self._screen, x, y)
        alpha = 255 - int(effectSec * 120)

        textBox.Print(text, 30, True, color, alpha)

        return False

    # 각 상속 객체에서 구현해야 할 세부 이펙트
    def _DrawEffect(self, effectSec):
        pass
