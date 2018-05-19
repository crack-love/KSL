import numpy as np
import os, sys
import functools
from PIL import Image
import cv2

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


def loadImageFiles(dirpath, fileList, isShow):
    imgList = []
    for file in fileList:
        img = Image.open(dirpath + "/" + file)
        img.load()
        data = np.asarray(img, dtype="uint8" )  # numpy로 변형
        imgList.append(data)
    
    if isShow:
        print("imgList Length: " + str(len(imgList)))
        print("img Shape: " + str(data.shape))

    return np.array(imgList)

def comp(a, b):
    a = a[:a.find('_')]
    b = b[:b.find('_')]
    return int(a) - int(b)

def loadSingleDataFromDir(dirpath, isShow):
    fileList = os.listdir(dirpath)
    
    leftFiles = []
    rightFiles = []

    for file in fileList:
        if file.find('L') != -1:
            leftFiles.append(file)
        elif file.find('R') != -1:
            rightFiles.append(file)
    
    leftFiles.sort(key=functools.cmp_to_key(comp))
    rightFiles.sort(key=functools.cmp_to_key(comp))

    leftImageList = loadImageFiles(dirpath, leftFiles, isShow)
    rightImageList = loadImageFiles(dirpath, rightFiles, isShow)

    spointData, label = loadDataFromFile(dirpath + "/Spoints.txt", isShow)

    if isShow:
        print()
    return spointData, leftImageList, rightImageList, label
