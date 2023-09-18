from .effect import Effect
from ui import TextBox


class PerfectHitEffect(Effect):
    def _DrawEffect(self, effectSec):
        return self._DrawPopupText(effectSec, "Perfect", "blue")
