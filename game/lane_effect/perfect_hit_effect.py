from .effect import Effect


class PerfectHitEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopupText(effectSec, "Perfect", "blue")
