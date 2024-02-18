import os
import json
import pygame
from time import sleep
from pygame import mixer
from pathlib import Path

from ..music.sheet import Sheet
from ..music.instrument import Instrument


class music_manager:
    def __init__(self):
        self._instrument = list()
        self._sheetByInstrument = dict(list())
        self._sheetChangeSound = None

        self._curInstrumentIdx = 0
        self._curSheetIdx = 0

        self._LoadInstrumentPitch()
        self._LoadInstrumentSound()
        self._LoadInstrumentImage()
        self._LoadSheet()
        self._LoadSheetChangeSound()

    def GetCurrentMusic(self):
        instrument = self._instrument[self._curInstrumentIdx]
        sheet = self._sheetByInstrument[instrument.Name][self._curSheetIdx]

        return instrument, sheet

    def GetInstrumentByName(self, name):
        for instrument in self._instrument:
            if instrument.Name == name:
                return instrument

    def GetInstrumentFirstSheet(self, instrumentName):
        return self._sheetByInstrument[instrumentName][0]

    # 악기 변경
    def ChangeInstrument(self, idxChange):
        self._curSheetIdx = 0

        if self._curInstrumentIdx + idxChange == len(self._instrument):
            self._curInstrumentIdx = 0
        elif self._curInstrumentIdx + idxChange == -1:
            self._curInstrumentIdx = len(self._instrument) - 1
        else:
            self._curInstrumentIdx += idxChange

    # 악기 변경에 따른 소리
    def ChangeInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("1")

    # 악기 선택에 따른 소리
    def SelectInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("1")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("2")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("3")

    # 악기 취소에 따른 소리
    def CancelInstrumentSound(self):
        self._instrument[self._curInstrumentIdx].PlayPitchSound("3")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("2")
        sleep(0.2)
        self._instrument[self._curInstrumentIdx].PlayPitchSound("1")
        
    # 악보 변경
    def ChangeSheet(self, idxChange):
        instrument = self._instrument[self._curInstrumentIdx]
        sheetLen = len(self._sheetByInstrument[instrument.Name])

        if self._curSheetIdx + idxChange == sheetLen:
            self._curSheetIdx = 0
        elif self._curSheetIdx + idxChange == -1:
            self._curSheetIdx = sheetLen - 1
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
            ext = os.path.splitext(instrumentJson)[-1].lower()
            if ext != ".json":
                continue

            instrumentName = Path(instrumentJson).stem
            instrumentJsonPath = os.path.join(instrumentPath, instrumentJson)

            # 일반 악기 추가
            instrument = Instrument(instrumentName)
            with open(instrumentJsonPath, encoding='UTF8') as file:
                pitchLaneData = json.load(file)
            instrument.SetPitchLane(pitchLaneData)
            self._instrument.append(instrument)

            # beat 연습 악기 추가 (그냥 깡통 악기)
            beatInstrument = Instrument(instrumentName + " - beatPractice")
            self._instrument.append(beatInstrument)

    # 각 악기별 계이름의 소리 추출
    def _LoadInstrumentSound(self):
        with open("config.json") as file:
            config = json.load(file)

        # 각 악기 이름 폴더에 대하여
        soundPath = os.path.join(os.getcwd(), config["musicSoundPath"])
        for instrumentName in os.listdir(soundPath):
            instrumentPitchPath = os.path.join(soundPath, instrumentName)

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
                targetInstrument.SetPitchSoundByPath(pitch, path)

            # beat 연습 악기에 대하여
            beatInstrument = None
            for instrument in self._instrument:
                if instrument.Name == instrumentName + " - beatPractice":
                    beatInstrument = instrument
                    break

            anySound = targetInstrument.GetAnyPitchSound()
            beatInstrument.SetPitchSoundByObject("notUsed", anySound)

    # 각 악기별 그림 추출
    def _LoadInstrumentImage(self):
        with open("config.json") as file:
            config = json.load(file)

        instrumentPath = os.path.join(os.getcwd(), config["musicInstrumentPath"])
        for instrumentImage in os.listdir(instrumentPath):
            ext = os.path.splitext(instrumentImage)[-1].lower()
            if ext != ".png":
                continue

            instrumentName = Path(instrumentImage).stem
            instrumentImagePath = os.path.join(instrumentPath, instrumentImage)

            instrumentImage = pygame.image.load(instrumentImagePath)
            for instrument in self._instrument:
                if instrument.Name == instrumentName:
                    instrument.SetImage(instrumentImage)

    # 각 악기별 연주 가능한 악보 추출
    def _LoadSheet(self):
        with open("config.json") as file:
            config = json.load(file)

        # 각 악기 이름 폴더에 대하여
        sheetPath = os.path.join(os.getcwd(), config["musicSheetPath"])
        for instrumentName in os.listdir(sheetPath):
            self._sheetByInstrument[instrumentName] = list()
            instrumentSheetPath = os.path.join(sheetPath, instrumentName)

            # 해당 폴더의 모든 악보를 추출
            for sheetJson in os.listdir(instrumentSheetPath):
                sheetName = Path(sheetJson).stem
                sheetJsonPath = os.path.join(instrumentSheetPath, sheetJson)
                with open(sheetJsonPath, encoding='UTF8') as file:
                    sheetData = json.load(file)

                sheet = Sheet(sheetName)
                sheet.MakeSheet(sheetData)
                self._sheetByInstrument[instrumentName].append(sheet)

                # beatPractice 악보에 대한 특별처리
                if sheetName == "beatPractice":
                    beatInstrumentName = instrumentName + " - beatPractice"
                    self._sheetByInstrument[beatInstrumentName] = list()
                    self._sheetByInstrument[beatInstrumentName].append(sheet)

                    beatInstrument = self.GetInstrumentByName(beatInstrumentName)
                    anySound = beatInstrument.GetAnyPitchSound()

                    pitchLaneData = dict(list())
                    for data in sheetData["악보"]:
                        pitch = data["계이름"]
                        if pitch == "쉼표":
                            continue

                        pitchLaneData[pitch] = [0]
                        beatInstrument.SetPitchSoundByObject(pitch, anySound)

                    beatInstrument.SetPitchLane(pitchLaneData)

    # 악보 변경 소리
    def _LoadSheetChangeSound(self):
        with open("config.json") as file:
            config = json.load(file)

        changeSoundPath = os.path.join(os.getcwd(), config["sheetChangeSound"])
        self._sheetChangeSound = mixer.Sound(changeSoundPath)
        self._sheetChangeSound.set_volume(0.2)
