import os
import sys
import json
from pathlib import Path

from ..music.instrument import Instrument


class InstrumentManager:
    def __init__(self):
        self._instrument = dict()

        self._LoadInstrumentPitch("config/instrument")
        self._LoadInstrumentSound("config/sound")

    def _LoadInstrumentPitch(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for instrumentJson in os.listdir(absPath):
            instrumentJsonPath = os.path.join(absPath, instrumentJson)

            instrument = Path(instrumentJson).stem
            self._instrument[instrument] = Instrument()

            with open(instrumentJsonPath, encoding='UTF8') as file:
                pitchLaneData = json.load(file)
                self._instrument[instrument].SetPitchLane(pitchLaneData)

    def _LoadInstrumentSound(self, relativePath):
        absPath = os.path.join(os.getcwd(), relativePath)
        if not os.path.exists(absPath):
            sys.exit("{0} path does not exist".format(absPath))

        for instrument in os.listdir(absPath):
            instrumentSoundPath = os.path.join(absPath, instrument)
            for soundMp3 in os.listdir(instrumentSoundPath):
                if instrument not in self._instrument:
                    continue

                pitch = Path(soundMp3).stem
                path = os.path.join(instrumentSoundPath, soundMp3)
                self._instrument[instrument].SetPitchSound(pitch, path)

    def GetInstrument(self, instrument):
        if instrument not in self._instrument:
            sys.exit("{0} instrument does not exist".format(instrument))

        return self._instrument[instrument]
