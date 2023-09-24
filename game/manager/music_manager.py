import os
import sys
import json
from pathlib import Path

from ..music.sheet import Sheet
from ..music.instrument import Instrument


class music_manager:
    def __init__(self):
        self._instrument = dict()
        self._sheet = dict()

        self._LoadInstrumentPitch("data/music/instrument")
        self._LoadInstrumentSound("data/music/sound")
        self._LoadSheet("data/music/sheet")

    def GetInstrument(self, instrument):
        if instrument not in self._instrument:
            sys.exit("{0} instrument does not exist".format(instrument))

        return self._instrument[instrument]

    def GetSheet(self, sheet):
        if sheet not in self._sheet:
            sys.exit("{0} sheet does not exist".format(sheet))

        return self._sheet[sheet]

    def _LoadInstrumentPitch(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for instrumentJson in os.listdir(absPath):
            instrumentName = Path(instrumentJson).stem
            instrumentJsonPath = os.path.join(absPath, instrumentJson)

            self._instrument[instrumentName] = Instrument()
            with open(instrumentJsonPath, encoding='UTF8') as file:
                pitchLaneData = json.load(file)
                self._instrument[instrumentName].SetPitchLane(pitchLaneData)

    def _LoadInstrumentSound(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for instrument in os.listdir(absPath):
            instrumentSoundPath = os.path.join(absPath, instrument)
            for sound in os.listdir(instrumentSoundPath):
                if instrument not in self._instrument:
                    continue

                pitch = Path(sound).stem
                path = os.path.join(instrumentSoundPath, sound)
                self._instrument[instrument].SetPitchSound(pitch, path)

    def _LoadSheet(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for sheetJson in os.listdir(absPath):
            sheetName = Path(sheetJson).stem
            sheetJsonPath = os.path.join(absPath, sheetJson)

            with open(sheetJsonPath, encoding='UTF8') as file:
                sheetData = json.load(file)
                sheet = Sheet(sheetName, sheetData)

                self._sheet[sheetName] = sheet
