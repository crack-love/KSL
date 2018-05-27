#from keras.preprocessing import image # image.load_img
#img = image.load_img()
import matplotlib.pyplot as plt # plt.imshow
import sys
import os
import os.path
import numpy as np
from LabelMapper import LabelMapper
import matplotlib

# 한글 폰트
nanum = "C:/Windows/Fonts/NanumGothicBold.ttf"
font_name = matplotlib.font_manager.FontProperties(fname=nanum).get_name()
matplotlib.rc('font', family=font_name)

def _plotWriteFile(path):
    '''
    this adding suffix .jpg
    https://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
    '''
    plt.savefig(path + '.jpg')

def plotSpointData(samplePath, rowSize, colSize, subidx, isImage):
    '''
    path=None 입력으로 plt.figure() 또는 plt.show() 호출만 가능
    '''
    if (samplePath != None):
        if os.path.isfile(samplePath) != True:
            print("not file")
            return

    rowSize=str(rowSize)
    colSize=str(colSize)
    subidx=str(subidx)

    if samplePath != None:
        splited = open(samplePath).readline().strip().split()
        date = splited[0]
        label = splited[1]
        frames = int(splited[2])
        spoints = int(splited[3])
        channels = int(splited[4])

        nowIdx = 5
        res = []
        # 행렬전치 (x:spoint, y:frames)
        # for s in range(spoints * channels):
        #   oneSpoint = []
        #   for f in range(frames):
        #       oneSpoint.append(float(splited[f * spoints * channels + s + nowIdx]))
        #       res.append(oneSpoint)
        for f in range(frames):
            oneFrame = []
            for i in range(channels):
                for j in range(spoints):
                    oneFrame.append(float(splited[nowIdx]))
                    nowIdx += 1
            res.append(oneFrame)
    
        pos = rowSize+colSize+subidx
        plt.subplot(pos)
        plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
        labelName = LabelMapper.getName(int(label))
        res = np.array(res)

        if isImage:
            res = np.transpose(res)
            plt.title(str(label) + '_' + labelName)
            plt.ylabel("L/R Spoints")
            plt.xlabel("Frame Sequence")
            plt.imshow(res)
        else:
            plt.title(date + ': ' + str(label) + '_' + labelName)
            plt.xlabel("Frame Sequence")
            plt.ylabel("Spoint Distance")
            plt.plot(res)

def plotSpointDataList(rootPath, rowSize, colSize, isImg, writePath):
    '''
    모든 라벨 Plot 파일로 출력

    rowSize, colSize 양식에 맞게 파일 개수 늘어남

    # Parameter
        rootPath : labelFolder(0_안녕하세요)의 상위 폴더
    '''
    labelFolders = os.listdir(rootPath)
    labelFolders = sorted(labelFolders)

    figureSize = rowSize * colSize
    labelSize = len(labelFolders)

    my_dpi = 144
    plt.figure(figsize=(1600/my_dpi, 900/my_dpi), dpi=my_dpi)
    for i in range(labelSize):
        labelFolder = labelFolders[i]
        path = os.path.join(rootPath, labelFolder)
        sampleList = os.listdir(path)
        lastSample = sampleList[len(sampleList) - 1]
        path = os.path.join(path, lastSample)
        path = os.path.join(path, 'Spoints.txt')
        index = (i % figureSize) + 1

        plotSpointData(path, rowSize, colSize, index, isImg)

        if index == figureSize or i == labelSize - 1:
            _plotWriteFile(writePath + '_' + str(i + 1))
            plt.figure(figsize=(1600/my_dpi, 900/my_dpi), dpi=my_dpi)
