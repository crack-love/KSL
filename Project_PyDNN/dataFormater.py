import numpy as np
import os, sys

#----------------------------------------------------------------
#  LABEL_SIZE is for one hot
#----------------------------------------------------------------
LABEL_SIZE = 5

#
# data, label을 일반 어레이로 반환하면 텐서플로에서 못알아먹기때문에
# np.array()로 wrap해서 내보내줘야한다.
# wrap해도 데이터 구조는 변경 없는것으로 보임
#

def relativePathToAbsolutePath(relative):
    scriptDirPath = os.path.dirname(os.path.realpath(__file__))
    return scriptDirPath + "/" + relative

def formatData(strdata, isShowLog):
    strdata = strdata.strip()

    items = strdata.split()
    
    date = items[0]
    label = int(items[1])
    frameSize = int(items[2])
    spointSize = int(items[3])
    channelSize = int(items[4])
    data = []

    dataSize = frameSize * spointSize * channelSize
    lastDataPos = dataSize + 5
    for i in range(5, lastDataPos):
        data.append(items[i])

    data = np.reshape(data, (frameSize, spointSize, channelSize))
    labelOneHot = np.zeros(LABEL_SIZE)
    labelOneHot[label] = 1

    if isShowLog:
        print("Format {0} Label{1} Frame{2} SPoint{3} Channel{4}"
        .format(date, label, frameSize, spointSize, channelSize))

    return np.array(data), np.array(labelOneHot)


def loadDataFromFile(file, isShowLog):
    fileStream = open(file)
    fileData = fileStream.readline()

    data, label = formatData(fileData, isShowLog)
    fileStream.close()

    return data, label
    

def loadDataFromDir(dirpath, isShowLog):
    fileList = os.listdir(dirpath)
    
    dataList = []
    labelList = []

    for file in fileList:
        data, label = loadDataFromFile(dirpath + "/" + file, isShowLog)
        dataList.append(data)
        labelList.append(label)

    return np.array(dataList), np.array(labelList)