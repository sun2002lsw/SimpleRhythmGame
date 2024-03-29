import etc
import pygame.display
import ui

from .manager.music_manager import *
from .rhythm_game import *


class MainMenu:
    def __init__(self, screen):
        self._screen = screen

        width, height = pygame.display.get_surface().get_size()
        self._width = width
        self._height = height

        # 필수 준비물 (악기, 악보)
        self._musicManager = music_manager()

        # 게임 한판 끝나면 메뉴로 돌아와서 처음부터 시작
        # 단, 악기 선택은 다시 하지 않음
        self._instrumentSelected = False
        while True:
            self._gameModeSelected = False
            self._sheetSelected = False
            self._autoPlay = False

            self._Start()

    # 메인 메뉴에서 순서대로 선택 진행
    def _Start(self):
        while True:
            self._ClearScreenWithTitle()
            sleep(0.3)

            # 악기 선택
            if self._instrumentSelected is False:
                self._StartInstrumentSelection()
                continue

            # 게임 모드 선택
            if self._gameModeSelected is False:
                self._StartGameModeSelection()
                continue

            # 악보 선택
            if self._sheetSelected is False:
                self._StartSheetSelection()
                continue

            # 모든 선택이 완료됨
            break

        # 게임 시작
        instrument, sheet = self._musicManager.GetCurrentMusic()
        self._StartGame(instrument, sheet)

    # 흰 바탕에 제목만 그리기
    def _ClearScreenWithTitle(self):
        self._screen.fill("white")

        x = self._width / 2
        y = self._height / 4
        titleImg = pygame.image.load("./game/main_menu_title.png")
        titleImg = pygame.transform.scale(titleImg, (x, y))

        rect = titleImg.get_rect()
        x -= titleImg.get_width() / 2
        y -= titleImg.get_height() / 2
        rect = rect.move((x, y))

        self._screen.blit(titleImg, rect)
        pygame.display.flip()

    # 악기 선택 과정
    def _StartInstrumentSelection(self):
        # 일단 beatPractice가 아닌 악기를 선택해서 시작
        while True:
            curInstrument, _ = self._musicManager.GetCurrentMusic()
            if "beatPractice" not in curInstrument.Name:
                break
            self._musicManager.ChangeInstrument(1)

        # 메뉴 그리기
        x = self._width * (1 / 2)
        y = self._height * (1 / 2)
        guideBox = ui.TextBox(self._screen, x, y)
        guideBox.Print("악기를 선택하세요", 50, True, "orange", 255)

        x = self._width * (3 / 8)
        y = self._height * (5 / 8)
        leftArrowBox = ui.TextBox(self._screen, x, y)
        leftArrowBox.Print("◀", 50, True, "black", 255)

        x = self._width * (5 / 8)
        y = self._height * (5 / 8)
        rightArrowBox = ui.TextBox(self._screen, x, y)
        rightArrowBox.Print("▶", 50, True, "black", 255)

        x = self._width * (1 / 2)
        y = self._height * (5 / 8)
        instrumentBox = ui.TextBox(self._screen, x, y)
        curInstrument, _ = self._musicManager.GetCurrentMusic()
        instrumentBox.Print(curInstrument.Name, 50, True, "black", 255)

        # 키보드로 악기 선택하기
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = event.key

                    # 숫자 입력을 다른 입력으로 전환
                    if key == pygame.K_1:
                        key = pygame.K_LEFT
                    elif key == pygame.K_2:
                        key = pygame.K_RIGHT
                    elif key == pygame.K_5:
                        key = pygame.K_ESCAPE

                    # esc: 게임 종료
                    if key is pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    # 악기 바꾸기
                    if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                        idxChange = (key - pygame.K_RIGHT) * 2 - 1
                        idxChange = -idxChange  # 이렇게 하면 왼쪽은 -1, 오른쪽은 +1

                        # beatPractice 악기를 제외하고 선택
                        while True:
                            self._musicManager.ChangeInstrument(idxChange)

                            curInstrument, _ = self._musicManager.GetCurrentMusic()
                            if "beatPractice" not in curInstrument.Name:
                                self._musicManager.ChangeInstrumentSound()
                                break

                        instrumentBox.Clear("white")
                        instrumentBox.Print(curInstrument.Name, 50, True, "black", 255)

                    # 악기 선택
                    if key is pygame.K_RETURN or key is pygame.K_0:
                        self._instrumentSelected = True
                        self._musicManager.SelectInstrumentSound()
                        return

    # 게임 모드 선택 과정
    def _StartGameModeSelection(self):
        self._buttons = []
        self._CreateButton(self._width / 2, self._ButtonHeight(1), "박자 연습", self._BeatPractice)
        self._CreateButton(self._width / 2, self._ButtonHeight(2), "음계 연습", self._PitchPractice)
        self._CreateButton(self._width / 2, self._ButtonHeight(3), "악곡 연주", self._PlayMusic)
        self._CreateButton(self._width / 2, self._ButtonHeight(4), "악곡 감상", self._ListenMusic)

        # 마우스 위치 초기화
        x = self._width / 2
        y = (self._ButtonHeight(2) + self._ButtonHeight(3)) / 2
        pygame.mouse.set_pos(x, y)

        # 마우스로 버튼 클릭하기
        while True:
            mousePos = pygame.mouse.get_pos()
            mousePressMove = pygame.mouse.get_pressed()
            mouseLeftPressMove = mousePressMove[0]  # 왼쪽 마우스를 누르고 움직일 때

            keys = pygame.key.get_pressed()
            keyboardPressing = keys[pygame.K_0]

            for event in pygame.event.get():
                # esc 눌러서 뒤로 가기
                escClick = event.type == pygame.KEYDOWN and (event.key is pygame.K_ESCAPE or event.key is pygame.K_5)
                if escClick:
                    self._instrumentSelected = False
                    self._musicManager.CancelInstrumentSound()
                    return

                # 숫자 입력을 버튼 선택으로 전환
                if event.type == pygame.KEYDOWN:
                    i = event.key - pygame.K_0
                    if 1 <= i <= 4:
                        pygame.mouse.set_pos(x, self._ButtonHeight(i))

                # 선택에 따른 행동 진행
                keyboardSelect = event.type == pygame.KEYUP and event.key is pygame.K_0
                mouseSelect = event.type == pygame.MOUSEBUTTONUP
                if keyboardSelect or mouseSelect:
                    if self._HandleButtonClick(mousePos):
                        return

                # 누르는 순간이나 누르고 움직이는 순간에 대한 이펙트 처리
                keyboardPress = event.type == pygame.KEYDOWN and event.key is pygame.K_0
                mousePress = event.type == pygame.MOUSEBUTTONDOWN
                if keyboardPress or keyboardPressing or mousePress or mouseLeftPressMove:
                    self._HandleButtonPressing(mousePos)
                else:
                    self._HandleButtonHovering(mousePos)

    # 버튼 추가
    def _CreateButton(self, x, y, text, clickFunc):
        button = ui.Button(self._screen, x, y, text, clickFunc)
        self._buttons.append(button)

    # i번째 버튼의 높이
    def _ButtonHeight(self, i):
        return self._height * (3 + i) / 8

    # 마우스를 버튼 위에 올렸을 때 처리
    def _HandleButtonHovering(self, mousePos):
        for button in self._buttons:
            button.Hovering(mousePos)

    # 마우스를 누른채 버튼 위에 올렸을 때 처리
    def _HandleButtonPressing(self, mousePos):
        for button in self._buttons:
            button.Pressing(mousePos)

    # 마우스를 클릭 했을 때 처리
    def _HandleButtonClick(self, mousePos):
        for button in self._buttons:
            if button.Click(mousePos):
                return True

        return False

    # 박자 연습 (지정된 악기와 악보를 그냥 연주)
    def _BeatPractice(self):
        curInstrument, _ = self._musicManager.GetCurrentMusic()
        beatInstrumentName = curInstrument.Name + " - beatPractice"

        beatInstrument = self._musicManager.GetInstrumentByName(beatInstrumentName)
        beatSheet = self._musicManager.GetInstrumentFirstSheet(beatInstrumentName)

        self._StartGame(beatInstrument, beatSheet)

    # 음계 연습 (지정된 악보를 연주)
    def _PitchPractice(self):
        _, curSheet = self._musicManager.GetCurrentMusic()

        # 지정된 악보를 찾기
        while curSheet.Name != "pitchPractice":
            self._musicManager.ChangeSheet(1)
            _, curSheet = self._musicManager.GetCurrentMusic()

        self._gameModeSelected = True
        self._sheetSelected = True

    # 악곡 연주 (따로 뭐 할거 없이 다음 단계 진행)
    def _PlayMusic(self):
        self._gameModeSelected = True

    # 악곡 감상 (autoPlay 켜주고 다음 단계 진행)
    def _ListenMusic(self):
        self._gameModeSelected = True
        self._autoPlay = True

    # 악보 선택 과정
    def _StartSheetSelection(self):
        # 일단 Practice가 아닌 악보를 선택해서 시작
        while True:
            _, curSheet = self._musicManager.GetCurrentMusic()
            if "Practice" not in curSheet.Name:
                break
            self._musicManager.ChangeSheet(1)

        # 메뉴 그리기
        x = self._width * (1 / 2)
        y = self._height * (1 / 2)
        guideBox = ui.TextBox(self._screen, x, y)
        guideBox.Print("악보를 선택하세요", 50, True, "orange", 255)

        x = self._width * (1 / 4)
        y = self._height * (5 / 8)
        leftArrowBox = ui.TextBox(self._screen, x, y)
        leftArrowBox.Print("◀", 50, True, "black", 255)

        x = self._width * (3 / 4)
        y = self._height * (5 / 8)
        rightArrowBox = ui.TextBox(self._screen, x, y)
        rightArrowBox.Print("▶", 50, True, "black", 255)

        x = self._width * (1 / 2)
        y = self._height * (5 / 8)
        sheetBox = ui.TextBox(self._screen, x, y)
        _, curSheet = self._musicManager.GetCurrentMusic()
        sheetBox.Print(curSheet.Name, 50, True, "black", 255)

        # 키보드로 악보 선택하기
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    key = event.key

                    # 숫자 입력을 다른 입력으로 전환
                    if key == pygame.K_1:
                        key = pygame.K_LEFT
                    elif key == pygame.K_2:
                        key = pygame.K_RIGHT
                    elif key == pygame.K_5:
                        key = pygame.K_ESCAPE

                    # esc: 뒤로 가기
                    if key is pygame.K_ESCAPE:
                        self._autoPlay = False
                        self._gameModeSelected = False
                        self._musicManager.CancelInstrumentSound()
                        return

                    # 악보 바꾸기
                    if key == pygame.K_LEFT or key == pygame.K_RIGHT:
                        self._musicManager.ChangeSheetSound()

                        idxChange = (key - pygame.K_RIGHT) * 2 - 1
                        idxChange = -idxChange  # 이렇게 하면 왼쪽은 -1, 오른쪽은 +1

                        # Practice 악보를 제외하고 선택
                        while True:
                            self._musicManager.ChangeSheet(idxChange)

                            _, curSheet = self._musicManager.GetCurrentMusic()
                            if "Practice" not in curSheet.Name:
                                break

                        sheetBox.Clear("white")
                        sheetBox.Print(curSheet.Name, 50, True, "black", 255)

                    # 악보 선택
                    if key is pygame.K_RETURN or key is pygame.K_0:
                        self._sheetSelected = True
                        self._musicManager.SelectInstrumentSound()
                        return

    # 게임 시작
    def _StartGame(self, instrument, sheet):
        etc.ScreenBlackOut(self._screen)  # 화면 어두워지기
        RhythmGame(self._screen, instrument, sheet, self._autoPlay)
