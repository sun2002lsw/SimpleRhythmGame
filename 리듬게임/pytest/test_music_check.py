from common import *
from pathlib import Path


# music 관련 경로에 있는 모든 파일은 유효한 json 파일이어야 함
def test_music_json_validation():
    config = getConfig()

    instrumentPath = getAbsPath(config["musicInstrumentPath"])
    invalidJsonFilePath = getInvalidJsonFilePath(instrumentPath)
    failMsg = "{0} file is invalid json file".format(invalidJsonFilePath)
    assert len(invalidJsonFilePath) == 0, failMsg

    sheetPath = getAbsPath(config["musicSheetPath"])
    invalidJsonFilePath = getInvalidJsonFilePath(sheetPath)
    failMsg = "{0} file is invalid json file".format(invalidJsonFilePath)
    assert len(invalidJsonFilePath) == 0, failMsg


# musicInstrumentPath 경로에 있는 악기 파일은
# 계이름이 겹쳐선 안 되고, 라인 집합도 겹치는게 없어야 함
def test_instrument_validation():
    config = getConfig()
    instrumentPath = getAbsPath(config["musicInstrumentPath"])

    for instrumentJson in os.listdir(instrumentPath):
        instrumentName = Path(instrumentJson).stem
        instrumentJsonPath = os.path.join(instrumentPath, instrumentJson)

        with open(instrumentJsonPath, encoding='UTF8') as file:
            pitchLaneData = json.load(file)

        pitchByLaneTuple = {}
        for pitch, lanes in pitchLaneData.items():
            lanes.sort()
            for idx, lane in enumerate(lanes):
                if idx > 0:
                    failMsg = ("duplicate lane detected. (instrument: {0}), (pitch: {1}), (lane: {2})"
                               .format(instrumentName, pitch, lanes[idx]))
                    assert lanes[idx - 1] != lanes[idx], failMsg

            laneTuple = tuple(lanes)
            failMsg = ("{0} instrument: {1} pitch and {2} pitch have same lanes"
                       .format(instrumentName, pitchByLaneTuple.get(laneTuple), pitch))
            assert laneTuple not in pitchByLaneTuple, failMsg

            pitchByLaneTuple[laneTuple] = pitch


# 악기 파일에 정의된 계이름은 sound 악기 폴더에 소리 파일이 있어야 함
def test_instrument_sound():
    pass
