from ..Effect import *


class EffectManager:
    def __init__(self, screen, laneLeftX, laneWidth, hitLineY):
        self._effect = dict()

        self._effect[EffectType.Danger] = DangerEffect(screen, laneLeftX, laneWidth, hitLineY)
        self._effect[EffectType.Miss] = MissEffect(screen, laneLeftX, laneWidth, hitLineY)
        self._effect[EffectType.GoodHit] = GoodHitEffect(screen, laneLeftX, laneWidth, hitLineY)
        self._effect[EffectType.PerfectHit] = PerfectHitEffect(screen, laneLeftX, laneWidth, hitLineY)
        self._effect[EffectType.Melting] = MeltingEffect(screen, laneLeftX, laneWidth, hitLineY)

    def StartOnce(self, effectType):
        self._effect[effectType].StartOnce()

    def Start(self, effectType):
        self._effect[effectType].Start()

    def Stop(self, effectType):
        self._effect[effectType].Stop()

    def Draw(self):
        for e in self._effect.values():
            e.Draw()
