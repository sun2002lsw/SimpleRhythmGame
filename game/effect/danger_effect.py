import pygame

from .effect import Effect


class DangerEffect(Effect):
    def _DrawEffect(self, effectSec):
        # 뭔가 놓칠 것 같은 노트에 대한 경고 이펙트를 추가하려 했는데,
        # 딱히 추가할 효과가 생각이 안 난다
        return True  
