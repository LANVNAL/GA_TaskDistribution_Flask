import re

def list2json(listData):
    length = len(listData)
    jsonData = {}
    for i in range(length):
        jsonData[i] = listData[i]
    return jsonData


