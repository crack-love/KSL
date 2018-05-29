#from keras.preprocessing import image # image.load_img
#img = image.load_img()
import matplotlib.pyplot as plt # plt.imshow
import sys
import os
import os.path
import numpy as np

def plotSpointData(path, colSize, rowSize, subidx, isImage, isShow, isWriteToFile, writePath):
    '''
    path=None 입력으로 plt.figure() 또는 plt.show() 호출만 가능
    '''
    if (path != None):
        if os.path.isfile(path) != True:
            print("not file")
            return

    rowSize=str(rowSize)
    colSize=str(colSize)
    subidx=str(subidx)

    if path != None:
        splited = open(path).readline().strip().split()
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
    
        plt.subplot(rowSize+colSize+subidx)
        plt.title(date + ": " + label)
        res = np.array(res)

        if isImage:
            plt.xlabel("L/R Spoints")
            plt.ylabel("Frame Sequence")
            plt.imshow(res)
        else:
            plt.xlabel("Frame Sequence")
            plt.ylabel("Spoint distance")
            plt.plot(res)
        
    if isShow: plt.show()
    #if isWriteToFile: plt.savefig('plot_datas.pdf', bbox_inchec='tight')
    if isWriteToFile: plt.savefig(writePath)
    #https://matplotlib.org/api/figure_api.html#matplotlib.figure.Figure
    

def plotSpointDataList(rootPath, colSize, isGraphShow, isImgShow, isWriteToFile, writePath):
    labelfolders = os.listdir(rootPath)
    dataSize = (len(labelfolders))
    if isGraphShow and isImgShow: colSize *= 2
    rowSize = int(dataSize / colSize)
    if rowSize * colSize < len(labelfolders): rowSize += 1
    
    index = 1
    plt.figure(str(isGraphShow) + str(isImgShow))
    for labelFolder in labelfolders:
        labelFolder = os.path.join(rootPath, labelFolder)
        sampleFolder = os.listdir(labelFolder)[0]
        sampleFolder = os.path.join(labelFolder, sampleFolder)
        dpath = os.path.join(sampleFolder, "Spoints.txt")
        #graph
        if isGraphShow:
            plotSpointData(dpath, colSize, rowSize, index, False, False, False, None)
            index += 1
        #img
        if isImgShow:
            plotSpointData(dpath, colSize, rowSize, index, True, False, False, None)
            index += 1

    if isWriteToFile:
        plotSpointData(None, 0, 0, 0, False, False, True, writePath)
    else:
        plotSpointData(None, 0, 0, 0, False, True, False, None)