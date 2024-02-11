import os
import json
from time import sleep
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

        self._LoadInstrumentPitch()
        self._LoadInstrumentSound()
        self._LoadSheet()
        self._LoadSheetChangeSound()

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

    # 악기 변경에 따른 소리
    def ChangeInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("도")

    # 악기 선택에 따른 소리
    def SelectInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("도")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("레")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("미")
        
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
    def _LoadInstrumentPitch(self):
        with open("config.json") as file:
            config = json.load(file)
            instrumentPath = os.path.join(os.getcwd(), config["musicInstrumentPath"])

        for instrumentJson in os.listdir(instrumentPath):
            instrumentName = Path(instrumentJson).stem
            instrumentJsonPath = os.path.join(instrumentPath, instrumentJson)

            instrument = Instrument(instrumentName)
            with open(instrumentJsonPath, encoding='UTF8') as file:
                pitchLaneData = json.load(file)
                instrument.SetPitchLane(pitchLaneData)

            self._instrument.append(instrument)

    # 각 악기별 계이름의 소리 추출
    def _LoadInstrumentSound(self):
        with open("config.json") as file:
            config = json.load(file)
            instrumentSoundPath = os.path.join(os.getcwd(), config["musicInstrumentSoundPath"])

        # 각 악기 이름 폴더에 대하여
        for instrumentName in os.listdir(instrumentSoundPath):
            instrumentPitchPath = os.path.join(instrumentSoundPath, instrumentName)

            # 해당하는 악기를 찾고
            targetInstrument = None
            for instrument in self._instrument:
                if instrument.Name == instrumentName:
                    targetInstrument = instrument
                    break

            if targetInstrument is None:
                continue

            # 소리 파일을 전부 할당
            for sound in os.listdir(instrumentPitchPath):
                pitch = Path(sound).stem
                path = os.path.join(instrumentPitchPath, sound)
                targetInstrument.SetPitchSound(pitch, path)

    # 각 악보 추출
    def _LoadSheet(self):
        with open("config.json") as file:
            config = json.load(file)
            sheetPath = os.path.join(os.getcwd(), config["musicSheetPath"])

        for sheetJson in os.listdir(sheetPath):
            sheetName = Path(sheetJson).stem
            sheetJsonPath = os.path.join(sheetPath, sheetJson)

            sheet = Sheet(sheetName)
            with open(sheetJsonPath, encoding='UTF8') as file:
                sheetData = json.load(file)
                sheet.MakeSheet(sheetData)

            self._sheet.append(sheet)

    def _LoadSheetChangeSound(self):
        with open("config.json") as file:
            config = json.load(file)
            changeSoundPath = os.path.join(os.getcwd(), config["sheetChangeSound"])

        self._sheetChangeSound = mixer.Sound(changeSoundPath)
        self._sheetChangeSound.set_volume(0.2)
