import os
import sys
import json
from pygame import mixer
from pathlib import Path

from ..music.sheet import Sheet
from ..music.instrument import Instrument


class music_manager:
    def __init__(self):
        self._instrument = list()
        self._sheet = list()
        self._sheetChangeSound = None

        self._curInstrumentIdx = 0
        self._curSheetIdx = 0

        self._LoadInstrumentPitch("data/music/instrument")
        self._LoadInstrumentSound("data/music/sound")
        self._LoadSheet("data/music/sheet")
        self._LoadSheetChangeSound("data/interface/sheetChange.wav")

    def GetCurrentMusic(self):
        return self._instrument[self._curInstrumentIdx], self._sheet[self._curSheetIdx]

    # 악기 변경
    def ChangeInstrument(self, idxChange):
        if self._curInstrumentIdx + idxChange == len(self._instrument):
            self._curInstrumentIdx = 0
        elif self._curInstrumentIdx + idxChange == -1:
            self._curInstrumentIdx = len(self._instrument) - 1
        else:
            self._curInstrumentIdx += idxChange

    def ChangeInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("도")

    # 악보 변경
    def ChangeSheet(self, idxChange):
        if self._curSheetIdx + idxChange == len(self._sheet):
            self._curSheetIdx = 0
        elif self._curSheetIdx + idxChange == -1:
            self._curSheetIdx = len(self._sheet) - 1
        else:
            self._curSheetIdx += idxChange

    def ChangeSheetSound(self):
        mixer.Sound.play(self._sheetChangeSound)

    # 각 악기별 계이름이 몇번 lane 인지 추출
    def _LoadInstrumentPitch(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for instrumentJson in os.listdir(absPath):
            instrumentName = Path(instrumentJson).stem
            instrumentJsonPath = os.path.join(absPath, instrumentJson)

            instrument = Instrument(instrumentName)
            with open(instrumentJsonPath, encoding='UTF8') as file:
                pitchLaneData = json.load(file)
                instrument.SetPitchLane(pitchLaneData)

            self._instrument.append(instrument)

        if len(self._instrument) == 0:
            sys.exit("there are no instrument")

    # 각 악기별 계이름의 소리 추출
    def _LoadInstrumentSound(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        # 각 악기 이름 폴더에 대하여
        for instrumentName in os.listdir(absPath):
            instrumentSoundPath = os.path.join(absPath, instrumentName)

            # 해당하는 악기를 찾고
            targetInstrument = None
            for instrument in self._instrument:
                if instrument.Name == instrumentName:
                    targetInstrument = instrument
                    break

            if targetInstrument is None:
                continue

            # 소리 파일을 전부 할당
            for sound in os.listdir(instrumentSoundPath):
                pitch = Path(sound).stem
                path = os.path.join(instrumentSoundPath, sound)
                targetInstrument.SetPitchSound(pitch, path)

    # 각 악보 추출
    def _LoadSheet(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for sheetJson in os.listdir(absPath):
            sheetName = Path(sheetJson).stem
            sheetJsonPath = os.path.join(absPath, sheetJson)

            sheet = Sheet(sheetName)
            with open(sheetJsonPath, encoding='UTF8') as file:
                sheetData = json.load(file)
                sheet.MakeSheet(sheetData)

            self._sheet.append(sheet)

        if len(self._sheet) == 0:
            sys.exit("there are no sheet")

    def _LoadSheetChangeSound(self, relativePath):
        soundFilePath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(soundFilePath):
            sys.exit("{0} path does not exist".format(soundFilePath))

        self._sheetChangeSound = mixer.Sound(soundFilePath)
        self._sheetChangeSound.set_volume(0.2)
