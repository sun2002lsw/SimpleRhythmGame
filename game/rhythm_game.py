import pygame
import sys

from . import music

DropSecs = [5, 3, 2, 1.5, 1, 0.5, 0.3, 0.1]


class RhythmGame:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 기본 빈 값 설정
        self._sheet = music.Sheet()
        self._laneCnt = 0
        self._dropSecIdx = 4

        self._start()
        
    # 기본 값들을 설정하고 게임 시작
    def _start(self):
        self._createSheet()
        self._laneCnt = 6 # self._sheet.GetLaneCnt()

        self._run()
        
    # 본격적인 게임 시작
    def _run(self):
        while True:
            self._drawGame()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # 게임 화면 출력
    def _drawGame(self):
        self._screen.fill((0, 0, 0))

        self._drawFrame()
        for i in range(0, self._laneCnt):
            self._drawNotes(i)
        
        pygame.display.flip()

    # 게임 틀 그리기
    def _drawFrame(self):
        x = self._width / 3
        y = self._height

        # 줄 긋는 순서 중요!
        for i in range(1, self._laneCnt):
            laneX = x + i * (x / self._laneCnt)
            pygame.draw.line(self._screen, "white", (laneX, 0), (laneX, y), 1)

        pygame.draw.line(self._screen, "red", (x, 0.8*y), (2*x, 0.8*y), 10)

        pygame.draw.line(self._screen, "white", (x, 0), (x, y), 5)
        pygame.draw.line(self._screen, "white", (2*x, 0), (2*x, y), 5)

    def _drawNotes(self, laneNum):
        pass

    # 악보 만들기 (이거 다른 모듈로 빼야겠지?)
    def _createSheet(self):
        pass
