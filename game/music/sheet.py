from copy import deepcopy

from .lane_note import LaneNote

EPSILON = 0.0000000000001
START_COUNT_DOWN_TIME = 2  # 시작할 때 준비 시간 카운트
BEAT_GAP = 1/16  # 박자랑 박자 사이에 쉬는 시간을 몇 박자로 할 것인가


class Sheet:
    def __init__(self, sheetName, sheetData):
        self._sheet = list()
        self._playedPitchBeginSec = dict()

        self._sheetName = sheetName
        self._ReadData(sheetData)

    def _ReadData(self, sheetData):
        oneBeatSec = 60 / sheetData["BPM"]
        self._beatGapSec = BEAT_GAP * oneBeatSec

        beginSec = START_COUNT_DOWN_TIME

        for data in sheetData["악보"]:
            pitch = data["계이름"]
            duration = data["박자"] * oneBeatSec

            note = (pitch, beginSec, duration)
            self._sheet.append(note)

            beginSec += duration + self._beatGapSec

    # 새롭게 게임 시작될 때 초기화
    def Ready(self):
        self._playedPitchBeginSec = dict()

    # 해당 악기에 맞는 lane 노트 반환
    def GetLaneNotesForInstrument(self, instrument):
        laneNotes = dict()
        for i in range(0, instrument.GetLaneCnt()):
            laneNotes[i] = list()

        for pitch, beginSec, duration in self._sheet:
            laneNote = LaneNote(beginSec, duration)

            laneSet = instrument.GetLaneSetByPitch(pitch)
            if laneSet is None:  # 쉼표 처리
                continue

            for laneNum in laneSet:
                # 리코더니깐 손가락을 뗐다 붙였다 하지 말고, 그냥 종료 시간 연장으로 계속 누르고 있기
                if len(laneNotes[laneNum]) > 0:
                    if abs(laneNotes[laneNum][-1].EndSec - beginSec) < self._beatGapSec + EPSILON:
                        laneNotes[laneNum][-1].EndSec = beginSec + duration
                        continue
                
                copyNote = deepcopy(laneNote)
                laneNotes[laneNum].append(copyNote)

        return laneNotes

    # 해당 시간의 계이름
    def GetPitchByCurrentSec(self, currentSec):
        for pitch, beginSec, duration in self._sheet:
            if currentSec < beginSec:
                break
            if beginSec <= currentSec <= beginSec + duration:
                return pitch

        return ""

    # 해당 시간에 딱 정확히 시작하는 계이름
    def GetStartPitchByCurrentSec(self, currentSec):
        for pitch, beginSec, duration in self._sheet:
            if beginSec in self._playedPitchBeginSec:
                continue

            if currentSec < beginSec:
                break

            if beginSec <= currentSec <= beginSec + 0.1:
                self._playedPitchBeginSec[beginSec] = True
                return pitch

        return ""

    def GetFinishSec(self):
        _, beginSec, duration = self._sheet[-1]
        return beginSec + duration + 5
