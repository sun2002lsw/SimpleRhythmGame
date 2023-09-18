from .effect import Effect


class MeltingEffect(Effect):
    def _DrawEffect(self, effectSec):
        if effectSec < 0.2:
            return False  # Stop() 할 때까지 계속 이펙트

        while effectSec > 0:
            self._DrawPopupText(effectSec, "Hit", "white")
            effectSec -= 0.2

        return False
