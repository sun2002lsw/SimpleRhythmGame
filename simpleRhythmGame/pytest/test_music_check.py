import pytest
from common import *
from pathlib import Path


@pytest.mark.order(3)
# music 관련 경로에 있는 모든 파일은 유효한 json 파일이어야 함
def test_music_json_validation():
    config = getConfig()

    instrumentPath = getAbsPath(config["musicInstrumentPath"])
    invalidJsonFilePath = getInvalidJsonFilePath(instrumentPath)
    failMsg = "{0} file is invalid json file".format(invalidJsonFilePath)
    assert len(invalidJsonFilePath) == 0, failMsg

    sheetPath = getAbsPath(config["musicSheetPath"])
    for instrumentName in os.listdir(sheetPath):
        instrumentSheetPath = os.path.join(sheetPath, instrumentName)
        invalidJsonFilePath = getInvalidJsonFilePath(instrumentSheetPath)
        failMsg = "{0} file is invalid json file".format(invalidJsonFilePath)
        assert len(invalidJsonFilePath) == 0, failMsg


@pytest.mark.order(4)
# musicInstrumentPath 경로에 있는 악기 파일은
# 계이름이 겹쳐선 안 되고, 라인 집합도 겹치는게 없어야 함
def test_instrument_validation():
    config = getConfig()
    instrumentPath = getAbsPath(config["musicInstrumentPath"])

    # 특정 악기에 대하여
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
                failMsg = ("{0} instrument - {1} pitch and {2} pitch have same lanes"
                           .format(instrumentName, pitchByLaneTuple.get(laneTuple), pitch))
                assert laneTuple not in pitchByLaneTuple, failMsg

                pitchByLaneTuple[laneTuple] = pitch


@pytest.mark.order(5)
# 악기 파일에 정의된 계이름은 sound 악기 폴더에 소리 파일이 있어야 함
def test_instrument_sound():
    config = getConfig()
    instrumentPath = getAbsPath(config["musicInstrumentPath"])
    soundPath = getAbsPath(config["musicSoundPath"])

    # 특정 악기에 대하여
    for instrumentJson in os.listdir(instrumentPath):
        instrumentName = Path(instrumentJson).stem
        instrumentJsonPath = os.path.join(instrumentPath, instrumentJson)

        # 계이름 목록을 가져오고
        with open(instrumentJsonPath, encoding='UTF8') as file:
            pitchLaneData = json.load(file)
            pitchList = pitchLaneData.keys()

        # 해당 악기의 음악 폴더에서 음악 파일 목록도 가져와서
        instrumentSoundPath = os.path.join(soundPath, instrumentName)
        failMsg = "{0} instrument sound file does not exist".format(instrumentName)
        assert os.path.exists(instrumentSoundPath), failMsg

        soundList = os.listdir(instrumentSoundPath)
        fileNameList = [Path(file).stem for file in soundList]
        fileNameDict = {fileName: 0 for fileName in fileNameList}

        # 계이름과 같은 이름의 파일이 있는지 확인
        for pitch in pitchList:
            failMsg = ("{0} instrument - {1} pitch sound file does not exist"
                       .format(instrumentName, pitch))
            assert pitch in fileNameDict, failMsg

        # 기본적으로 필요한 필수 소리 파일
        for pitch in ["1", "2", "3"]:
            failMsg = "{0} instrument - default sound file does not exist".format(instrumentName)
            assert pitch in fileNameDict, failMsg


@pytest.mark.order(6)
# 각 악기에 대하여 자기만의 악보가 있어야 함
def test_instrument_sheet():
    config = getConfig()
    instrumentPath = getAbsPath(config["musicInstrumentPath"])
    sheetPath = getAbsPath(config["musicSheetPath"])

    # 특정 악기에 대하여
    for instrumentJson in os.listdir(instrumentPath):
        instrumentName = Path(instrumentJson).stem
        instrumentSheetPath = os.path.join(sheetPath, instrumentName)

        sheetList = os.listdir(instrumentSheetPath)
        fileNameList = [Path(file).stem for file in sheetList]
        fileNameDict = {fileName: 0 for fileName in fileNameList}

        # 기본적으로 필요한 필수 악보 파일
        for sheet in ["beatPractice", "pitchPractice"]:
            failMsg = "{0} instrument - default sheet file does not exist".format(instrumentName)
            assert sheet in fileNameDict, failMsg

        # 기본 파일을 제외하고 최소 1개의 파일은 있어야 함
        failMsg = "{0} instrument - need more sheet file".format(instrumentName)
        assert len(fileNameList) > 2, failMsg
