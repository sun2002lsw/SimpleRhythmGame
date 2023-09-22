from .effect import Effect

DRAW_INTERVAL = 0.1


class MeltingEffect(Effect):
    def _DrawEffect(self, effectSec):
        if effectSec < DRAW_INTERVAL:
            return False  # 시작한지 얼마 안 되었으면 출력 안 함

        effectSec = effectSec % DRAW_INTERVAL  # 이펙트를 0.1초 주기로 반복
        self._DrawPopCircle(effectSec, DRAW_INTERVAL, 30)

        return False  # Stop() 할 때까지 계속 이펙트
