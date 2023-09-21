from .effect import Effect


class GoodHitEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopupText(effectSec, "Good", "green")
