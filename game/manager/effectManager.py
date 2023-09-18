from ..Effect import *


class EffectManager:
    def __init__(self, screen, laneLeftX, laneWidth, hitLineY):
        self._effect = dict()

        self._effect[EffectType.Danger] = DangerEffect(screen, laneLeftX, laneWidth, hitLineY)
        self._effect[EffectType.Miss] = MissEffect(screen, laneLeftX, laneWidth, hitLineY)

    def Start(self, effectType):
        self._effect[effectType].Start()

    def Draw(self):
        for e in self._effect.values():
            e.Draw()
