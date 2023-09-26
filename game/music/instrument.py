from pygame import mixer


class Instrument:
    def __init__(self, name):
        self.Name = name

        self._laneCnt = 0
        self._laneSetByPitch = dict()
        self._pitchByLaneSet = dict()
        self._soundByPitch = dict()
        self._pressingLanes = dict()
        self._lastPlayedSound = None

    # 새롭게 게임 시작될 때 초기화
    def Ready(self):
        self._pressingLanes = dict()

    def SetPitchLane(self, pitchLaneData):
        for pitch, lanes in pitchLaneData.items():
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

    def GetLaneSetByPitch(self, pitch):
        if pitch not in self._laneSetByPitch:
            return None

        return self._laneSetByPitch[pitch]

    # 키를 누름으로서 소리 재생
    def PlayKeyDownSound(self, lane):
        self._pressingLanes[lane] = True
        self._PlaySoundByPressing()
        
    # 키를 뗌으로서 소리 재생
    def PlayKeyUpSound(self, lane):
        self._pressingLanes[lane] = False
        self._PlaySoundByPressing()

    def _PlaySoundByPressing(self):
        pressingLanes = list()
        for lane, isPressing in self._pressingLanes.items():
            if isPressing:
                pressingLanes.append(lane)

        laneSet = frozenset(pressingLanes)
        if laneSet not in self._pitchByLaneSet:
            return

        pitch = self._pitchByLaneSet[laneSet]
        self.PlayPitchSound(pitch)

    # 해당 pitch에 맞는 소리 재생
    def PlayPitchSound(self, pitch):
        if pitch not in self._soundByPitch:
            return

        if self._lastPlayedSound is not None:
            mixer.Sound.stop(self._lastPlayedSound)

        sound = self._soundByPitch[pitch]
        mixer.Sound.play(sound)
        self._lastPlayedSound = sound
