from .GA import main as GAmain
from .GA import getResultData
from .util import list2json
import json
from .draw import drawFromData

resultData = []


def runGA(**kwargs):
    global resultData
    GAmain(**kwargs)
    resultData = getResultData()
    return resultData


def resultData(resultData):
    jsonResult = list2json(resultData)
    print(jsonResult)
    return jsonResult


def getData():
    return resultData


def drawScatter():
    filename = drawFromData()
    return filename

