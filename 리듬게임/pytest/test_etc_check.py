from common import *


def test_config_exist():
    configPath = getAbsPath("config.json")

    failMsg = "config file does not exist in {0}".format(configPath)
    assert os.path.exists(configPath), failMsg

    invalidJsonFilePath = getInvalidJsonFilePath(configPath)
    failMsg = "{0} file is invalid json file".format(invalidJsonFilePath)
    assert len(invalidJsonFilePath) == 0, failMsg


def test_interface_sound_files_exist():
    config = getConfig()

    for key, path in config.items():
        failMsg = "{0}: {1} path does not exist".format(key, path)
        resourcePath = getAbsPath(path)

        assert os.path.exists(resourcePath), failMsg

