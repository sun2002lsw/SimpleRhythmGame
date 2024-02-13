import copy
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
        self._sheetByInstrument = dict(list())
        self._beatPracticePitch = list()
        self._sheetChangeSound = None

        self._curInstrumentIdx = 0
        self._curSheetIdx = 0

        self._LoadInstrumentPitch()
        self._LoadInstrumentSound()
        self._LoadSheet()
        self._LoadSheetChangeSound()

        self._CreateBeatPracticeInstrument()

    def ResetCurrentMusic(self):
        self._curInstrumentIdx = 0
        self._curSheetIdx = 0

    def GetCurrentMusic(self):
        instrument = self._instrument[self._curInstrumentIdx]
        sheet = self._sheetByInstrument[instrument.Name][self._curSheetIdx]

        return instrument, sheet

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
            soundPath = os.path.join(os.getcwd(), config["musicSoundPath"])

        # 각 악기 이름 폴더에 대하여
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

    # 각 악기별 연주 가능한 악보 추출
    def _LoadSheet(self):
        with open("config.json") as file:
            config = json.load(file)
            sheetPath = os.path.join(os.getcwd(), config["musicSheetPath"])

        # 각 악기 이름 폴더에 대하여
        for instrumentName in os.listdir(sheetPath):
            instrumentSheetPath = os.path.join(sheetPath, instrumentName)

            # 해당 폴더의 모든 악보를 추출
            for sheetJson in os.listdir(instrumentSheetPath):
                sheetName = Path(sheetJson).stem
                sheetJsonPath = os.path.join(sheetPath, sheetJson)

                sheet = Sheet(sheetName)
                with open(sheetJsonPath, encoding='UTF8') as file:
                    sheetData = json.load(file)
                    sheet.MakeSheet(sheetData)

                self._sheetByInstrument[instrumentName].append(sheet)

                # beatPractice 악보에 대한 특별처리
                if sheetName == "beatPractice":
                    for data in sheetData["악보"]:
                        pitch = data["계이름"]
                        self._beatPracticePitch.append(pitch)

    # 악보 변경 소리
    def _LoadSheetChangeSound(self):
        with open("config.json") as file:
            config = json.load(file)
            changeSoundPath = os.path.join(os.getcwd(), config["sheetChangeSound"])

        self._sheetChangeSound = mixer.Sound(changeSoundPath)
        self._sheetChangeSound.set_volume(0.2)

    # 각 악기들에 대하여 박자 연습 전용 악기를 만들어준다
    def _CreateBeatPracticeInstrument(self):
        pitchLaneData = dict()
        for pitch in self._beatPracticePitch:
            if pitch != "쉼표":
                pitchLaneData[pitch] = [0]  # 박자연습은 항상 0번 레인만 사용

        beatInstruments = list()
        for instrument in self._instrument:
            beatInstrumentName = instrument.Name + " - beatPractice"
            beatInstrument = Instrument(beatInstrumentName)
            beatInstrument.SetPitchLane(pitchLaneData)

            # 어떤 박자를 연주하건 소리는 중요하지 않다
            sound = instrument.GetAnyPitchSound()
            for pitch in self._beatPracticePitch:
                beatInstrument.SetPitchSoundByObject(pitch, sound)

            beatInstruments.append(beatInstrument)

        # 새롭게 제작된 박자 연습 전용 악기들을 추가
        self._instrument.extend(beatInstruments)
