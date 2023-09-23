import sys
from copy import deepcopy

from .note import Note

START_COUNT_DOWN_TIME = 2  # 시작할 때 준비 시간 카운트
EPSILON = 0.0000000000001

class Sheet:
    def __init__(self, sheetName, sheet):
        self._sheetName = sheetName
        self._sheet = sheet

        self._CheckValidation()

    # 계이름 겹치는 시간은 없는지 확인
    def _CheckValidation(self):
        curSec = 0

        for pitchInfo in self._sheet:
            beginSec = pitchInfo["시작(초)"]
            curSecWithEpsilon = curSec - EPSILON  # 1.2 + 0.3 하면 1.500000002 나옴;;
            if beginSec < curSecWithEpsilon:
                errorStr = "{0} overlapped time detected on {1} sec".format(self._sheetName, beginSec)
                sys.exit(errorStr)

            duration = pitchInfo["유지(초)"]
            curSec = beginSec + duration

    # 해당 악기에 맞는 lane별 노트 반환
    def GetLaneNotesForInstrument(self, instrument):
        laneNotes = dict()
        for i in range(0, instrument.GetLaneCnt()):
            laneNotes[i] = list()

        for pitchInfo in self._sheet:
            pitch = pitchInfo["계이름"]
            beginSec = pitchInfo["시작(초)"] + START_COUNT_DOWN_TIME
            duration = pitchInfo["유지(초)"]

            note = Note(beginSec, duration)

            for laneNum in instrument.GetLaneSetByPitch(pitch):
                # 바로 앞의 노트랑 이어지면, 새로운 노트 넣지 말고 그냥 시간 연장
                if len(laneNotes[laneNum]) > 0:
                    if abs(laneNotes[laneNum][-1].EndSec - beginSec) < EPSILON:
                        laneNotes[laneNum][-1].EndSec += duration
                        continue
                
                copyNote = deepcopy(note)
                laneNotes[laneNum].append(copyNote)

        return laneNotes

    # 해당 시간의 계이름
    def GetPitchByCurrentSec(self, currentSec):
        for pitchInfo in self._sheet:
            pitch = pitchInfo["계이름"]
            beginSec = pitchInfo["시작(초)"] + START_COUNT_DOWN_TIME
            duration = pitchInfo["유지(초)"]

            if currentSec < beginSec:
                break
            if beginSec <= currentSec <= beginSec + duration:
                return pitch

        return ""
