from .effect import Effect


class MissEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopupText(effectSec, "Miss", "red")
