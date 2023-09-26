import os
import sys
import json
from pathlib import Path

from ..music.sheet import Sheet
from ..music.instrument import Instrument


class music_manager:
    def __init__(self):
        self._instrument = list()
        self._sheet = list()

        self._curInstrumentIdx = 0
        self._curSheetIdx = 0

        self._LoadInstrumentPitch("data/music/instrument")
        self._LoadInstrumentSound("data/music/sound")
        self._LoadSheet("data/music/sheet")

    def GetCurrentMusic(self):
        return self._instrument[self._curInstrumentIdx], self._sheet[self._curSheetIdx]

    # 악기 변경
    def ChangeInstrument(self, idxChange):
        newIdx = self._curInstrumentIdx + idxChange
        if newIdx < 0:
            newIdx = newIdx + len(self._instrument)
        elif newIdx >= len(self._instrument):
            newIdx = newIdx - len(self._instrument)

        self._curInstrumentIdx = newIdx

    # 악보 변경
    def ChangeSheet(self, idxChange):
        newIdx = self._curSheetIdx + idxChange
        if newIdx < 0:
            newIdx = newIdx + len(self._sheet)
        elif newIdx >= len(self._instrument):
            newIdx = newIdx - len(self._sheet)

        self._curSheetIdx = newIdx

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
