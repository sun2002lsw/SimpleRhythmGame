from pygame import mixer


class Instrument:
    def __init__(self):
        self._laneSetByPitch = dict()
        self._pitchByLaneSet = dict()
        self._soundByPitch = dict()
        self._laneCnt = 0

    def SetPitchLane(self, jsonData):
        for pitch, lanes in jsonData.items():
            laneSet = frozenset(lanes)

            self._laneSetByPitch[pitch] = laneSet
            self._pitchByLaneSet[laneSet] = pitch

        self._SetLaneCnt()

    def SetPitchSound(self, pitch, soundPath):
        sound = mixer.Sound(soundPath)
        self._soundByPitch[pitch] = sound

    def _SetLaneCnt(self):
        maxLane = 0
        for laneSet in self._laneSetByPitch.values():
            for lane in laneSet:
                maxLane = max(maxLane, lane)

        self._laneCnt = maxLane + 1

    def GetLaneCnt(self):
        return self._laneCnt

    def GetPitchByLaneSet(self, laneSet):
        return self._pitchByLaneSet[laneSet]

    def GetLaneSetByPitch(self, pitch):
        return self._laneSetByPitch[pitch]

    def PlayPitchSound(self, pitch):
        if pitch not in self._soundByPitch:
            return

        sound = self._soundByPitch[pitch]
        mixer.Sound.play(sound)
