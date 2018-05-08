import numpy as np
import os, sys

# -------------------------------------------------------------- 
#
# LABEL_SIZE: is for one hot
#
# np.array():
# data, label을 일반 어레이로 반환하면 텐서플로에서 못알아먹기때문에
# np.array()로 wrap해서 내보내줘야한다.
# wrap해도 데이터 구조는 변경 없는것으로 보임
#
#----------------------------------------------------------------

LABEL_SIZE = 5

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


## return single data
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

    ## 로드 결과 각 라벨 몇개씩인지 프린트
    labelCnt = [0] * LABEL_SIZE
    for i in range(0, len(labelList)):
        labelIdx = np.argmax(labelList[i])
        labelCnt[labelIdx] += 1
    print(os.path.basename(dirpath) + ": " + str(labelCnt))

    return np.array(dataList), np.array(labelList)

def loadLabelFile(path, isShow = True):
    f = open(path)

    labelList = { -1:'None' }

    for line in f:
        if len(line) > 3:
            tokens = line.split()
            
            number = int(tokens[0])
            name = str(tokens[1])

            labelList[number] = name

            if (isShow):
                print(str(number) + ': ' + str(name))

    return labelList