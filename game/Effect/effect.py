import pygame
from enum import Enum, auto


class EffectType(Enum):
    Danger = auto()  # 노트가 히트라인을 지나친 상황
    Miss = auto()  # 노트가 완전히 지나쳐서 놓친 상황
    Hit = auto()  # 타이밍 맞게 눌러서 맞춘 상황
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

    def _DrawEffect(self, effectSec):
        pass
