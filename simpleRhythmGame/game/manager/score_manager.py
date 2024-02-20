import pygame
from enum import Enum, auto
from collections import defaultdict

from ui import TextBox


class ScoreManager:
    def __init__(self, screen, width, height):
        self._screen = screen
        self._width = width
        self._height = height

        comboX = width / 2
        comboY = height / 3
        self._comboStrBox = TextBox(self._screen, comboX, comboY - 70)
        self._comboDrawBox = TextBox(self._screen, comboX, comboY)

        scoreX = width * 5 / 6
        scoreY = height / 2
        self._scoreStrBox = TextBox(self._screen, scoreX, scoreY - 70)
        self._scoreDrawBox = TextBox(self._screen, scoreX, scoreY)

        self._combo = 0
        self._comboTick = 0
        self._score = 0

        self._lastPitch = None
        self._hitCntByPitch = defaultdict(int)
        self._missCntByPitch = defaultdict(int)

    def AddComboState(self, comboState, pitch):
        if comboState == comboState.NoChange:
            return

        # miss
        if comboState == ComboState.Miss:
            self._AddMissPitch(pitch)
            self._combo = 0
            return

        # hit
        self._AddHitPitch(pitch)

        self._combo += 1
        self._score += self._combo
        if comboState == ComboState.Perfect:
            self._score += self._combo

        self._comboTick = pygame.time.get_ticks()

    def _AddMissPitch(self, pitch):
        if self._lastPitch == pitch:
            return
        if pitch == "" or pitch == "쉼표":
            return

        self._lastPitch = pitch
        self._missCntByPitch[pitch] += 1

    def _AddHitPitch(self, pitch):
        if self._lastPitch == pitch:
            return
        if pitch == "" or pitch == "쉼표":
            return

        self._lastPitch = pitch
        self._hitCntByPitch[pitch] += 1

    def Draw(self):
        self._DrawCombo()
        self._DrawScore()

    def _DrawCombo(self):
        effectSec = (pygame.time.get_ticks() - self._comboTick) / 1000
        strSize = int(max(100 - effectSec * 100, 50))
        alpha = int(max(255 - effectSec * 100, 50))

        self._comboStrBox.Print("COMBO", 50, True, "white", alpha)
        self._comboDrawBox.Print(str(self._combo), strSize, True, "white", alpha)

    def _DrawScore(self):
        self._scoreStrBox.Print("SCORE", 50, True, "white", 255)
        self._scoreDrawBox.Print(str(self._score), 50, True, "white", 255)

    def DrawResult(self):
        hitKeys = self._hitCntByPitch.keys()
        missKeys = self._missCntByPitch.keys()
        allKeys = set(hitKeys) | set(missKeys)
        pitchCnt = len(allKeys)

        resultByPitch = dict()
        for key in allKeys:
            hitCnt = self._hitCntByPitch[key]
            missCnt = self._missCntByPitch[key]
            totalCnt = hitCnt + missCnt
            accuracy = hitCnt / totalCnt * 100

            resultByPitch[key] = (hitCnt, totalCnt, accuracy)

        # 정확도순으로 정렬. 똑같으면 히트수 정렬. 똑같으면 이름수 정렬
        sortedByName = sorted(resultByPitch.items(), key=lambda items: items[1][0], reverse=True)
        sortedByTotalCnt = sorted(sortedByName, key=lambda items: items[1][1], reverse=True)
        sortedByAccuracy = sorted(sortedByTotalCnt, key=lambda items: items[1][2], reverse=True)

        # 음표별 결과 쓰기
        widthOffset = self._width / ((pitchCnt + 3) * 2)
        boxWidth = 2 * widthOffset

        heightOffset = self._height / 4 / 6
        boxHeight = 2 * heightOffset

        beginX = boxWidth
        endX = self._width - boxWidth

        beginY = boxHeight
        endY = beginY + 2 * boxHeight
        middleY = (beginY + endY) / 2

        textY1 = beginY + heightOffset
        textY2 = textY1 + boxHeight

        # 사각 틀을 그리기 전에 표기용 칸부터 색칠한다 (사각 틀 경계선이 색칠칸 위에 출력 되도록)
        rect = pygame.Rect(beginX, beginY, boxWidth, 2 * boxHeight)
        pygame.draw.rect(self._screen, "aqua", rect)

        # 사각 틀 그리기
        pygame.draw.line(self._screen, "white", (beginX, beginY), (beginX, endY), 3)
        pygame.draw.line(self._screen, "white", (beginX, beginY), (endX, beginY), 3)
        pygame.draw.line(self._screen, "white", (beginX, endY), (endX, endY), 3)
        pygame.draw.line(self._screen, "white", (endX, beginY), (endX, endY), 3)

        # 틀 안에 경계선 그리기
        pygame.draw.line(self._screen, "white", (beginX, middleY), (endX, middleY), 1)
        for i in range(pitchCnt):
            x = beginX + (i + 1) * boxWidth
            pygame.draw.line(self._screen, "white", (x, beginY), (x, endY), 1)

        pygame.display.flip()

        # 가장 왼쪽 상자는 표기용 상자
        x = beginX + widthOffset
        TextBox(self._screen, x, textY1).Print("계이름", 35, True, "white", 255)
        TextBox(self._screen, x, textY2).Print("맞춤/전체", 25, True, "white", 255)

        # 나머지 상자들 채워 넣기
        for i, pitchInfo in enumerate(sortedByAccuracy):
            pitchStr = pitchInfo[0]
            hitCnt = pitchInfo[1][0]
            totlaCnt = pitchInfo[1][1]
            resultStr = str(hitCnt) + "/" + str(totlaCnt)

            x = (2 + i) * boxWidth + widthOffset
            TextBox(self._screen, x, textY1).Print(pitchStr, 30, True, "yellow", 255)
            TextBox(self._screen, x, textY2).Print(resultStr, 30, True, "white", 255)

        # 최고의 플레이
        x = self._width * (1 / 3)
        y = self._height * (1 / 2)
        TextBox(self._screen, x, y).Print("많이 성공한 계이름", 50, True, "aqua", 255)

        yOffset = self._height / 16
        y += yOffset
        for i in range(3):
            rank = i + 1
            nextY = y + rank * yOffset

            try:
                pitchInfo = sortedByAccuracy[i]
            except IndexError:
                continue

            pitch = pitchInfo[0]
            accuracy = pitchInfo[1][2]

            resultStr = "{}. {}({:.1f}%)".format(rank, pitch, accuracy)
            TextBox(self._screen, x, nextY).Print(resultStr, 30, True, "white", 255)

        # 최악의 플레이
        x = self._width * (2 / 3)
        y = self._height * (1 / 2)
        TextBox(self._screen, x, y).Print("노력이 필요한 계이름", 50, True, "red", 255)

        yOffset = self._height / 16
        y += yOffset
        for i in range(3):
            rank = i + 1
            nextY = y + rank * yOffset

            try:
                pitchInfo = sortedByAccuracy[-rank]
            except IndexError:
                continue

            pitch = pitchInfo[0]
            accuracy = pitchInfo[1][2]

            resultStr = "{}. {}({:.1f}%)".format(rank, pitch, accuracy)
            TextBox(self._screen, x, nextY).Print(resultStr, 30, True, "white", 255)


class ComboState(Enum):
    Perfect = auto()    # 콤보 증가
    Good = auto()       # 콤보 증가
    Miss = auto()       # 콤보 초기화
    NoChange = auto()   # 변화 없음
