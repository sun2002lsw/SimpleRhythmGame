from .effect import Effect


class ExplosionEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopCircle(effectSec, 0.5, 10)
