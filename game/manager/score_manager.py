import pygame
from enum import Enum, auto

from ui import TextBox


class ScoreManager:
    def __init__(self, screen, width, height):
        self._screen = screen

        comboX = width / 2
        comboY = height / 3
        self._comboStrBox = TextBox(self._screen, comboX, comboY - 70)
        self._comboDrawBox = TextBox(self._screen, comboX, comboY)

        scoreX = width * 5 / 6
        scoreY = height / 2
        self._scoreStrBox = TextBox(self._screen, scoreX, scoreY - 70)
        self._scoreDrawBox = TextBox(self._screen, scoreX, scoreY)

        self._combo = 0
        self._comboTick = 0
        self._score = 0

    def AddComboState(self, comboState):
        if comboState == comboState.NoChange:
            return

        if comboState == ComboState.Miss:
            self._combo = 0
            return

        # combo hit
        self._combo += 1
        self._score += self._combo
        self._comboTick = pygame.time.get_ticks()

        if comboState == ComboState.Perfect:
            self._score += self._combo

    def Draw(self):
        self._DrawCombo()
        self._DrawScore()

    def _DrawCombo(self):
        effectSec = (pygame.time.get_ticks() - self._comboTick) / 1000
        strSize = int(max(100 - effectSec * 100, 50))
        alpha = int(max(255 - effectSec * 100, 50))

        self._comboStrBox.Print("COMBO", 50, True, "white", alpha)
        self._comboDrawBox.Print(str(self._combo), strSize, True, "white", alpha)

    def _DrawScore(self):
        self._scoreStrBox.Print("SCORE", 50, True, "white", 255)
        self._scoreDrawBox.Print(str(self._score), 50, True, "white", 255)


class ComboState(Enum):
    Perfect = auto()    # 콤보 증가
    Good = auto()       # 콤보 증가
    Miss = auto()       # 콤보 초기화
    NoChange = auto()   # 변화 없음
