from .effect import Effect
from ui import TextBox


class MissEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopupText(effectSec, "Miss", "red")
