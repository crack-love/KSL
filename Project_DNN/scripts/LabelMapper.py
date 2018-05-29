''' ---------------------------------------------------

# LABEL Mapper:
  클래스 메서드로 접근 가능

--------------------------------------------------- '''

import os
from Path import Path

class _LabelMapper():
    # variables
    _itosDic = {}
    _stoiDic = {}

    def __init__(self):
        self._load()

    # set func
    def _set(self, intKey, strValue):
        self._itosDic[int(intKey)] = str(strValue)
        self._stoiDic[str(strValue)] = int(intKey)

    # get func
    def getName(self, intKey):
        return self._itosDic[intKey]

    def getIndex(self, strValue):
        return self._stoiDic[strValue]

    # load label file
    def _load(self):
        labelPath = Path.get('data') + '\\LABEL.txt'
        fs = open(labelPath)
        for line in fs:
            splited = line.strip().split()
            if len(splited) == 2:
                idx = splited[0]
                name = splited[1]
                self._set(idx, name)

LabelMapper = _LabelMapper()