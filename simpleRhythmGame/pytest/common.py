import os
import json


def getAbsPath(relativePath):
    return os.path.join(os.getcwd(), "simpleRhythmGame/" + relativePath)


def getConfig():
    configPath = getAbsPath("config.json")

    with open(configPath) as file:
        return json.load(file)


def getInvalidJsonFilePath(path):
    if os.path.isdir(path):
        return checkDirJsonFiles(path)
    else:
        return checkOneJsonFile(path)


def checkOneJsonFile(path):
    with open(path, encoding='UTF8') as file:
        try:
            json.load(file)
        except ValueError as e:
            return os.path.basename(file.name)

    return ""


def checkDirJsonFiles(path):
    for jsonFile in os.listdir(path):
        jsonFilePath = os.path.join(path, jsonFile)

        with open(jsonFilePath, encoding='UTF8') as file:
            try:
                json.load(file)
            except ValueError as e:
                return os.path.basename(file.name)

    return ""
