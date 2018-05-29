import numpy as np
import os, sys
import functools
import matplotlib.pyplot as plt # plt.imshow
import scripts.interfaceUtils as util #input(debug)
from keras.preprocessing import image # image.load_img
import defines

#import cv2

# -------------------------------------------------------------- 
#
# LABEL_SIZE: is for one hot
#
# np.array():
# data, label을 일반 어레이로 반환하면 텐서플로에서 못알아먹기때문에
# np.array()로 wrap해서 내보내줘야한다.
# wrap해도 데이터 구조는 변경 없는것으로 보임
#
# label is one hot
#
# 이미지 읽기를 위한 필요 패키지 설치 : pip install Pillow
#
#----------------------------------------------------------------

def _formatData(strdata, isShowLog):
    strdata = strdata.strip()

    items = strdata.split()
    
    date = items[0]
    label = int(items[1])
    frameSize = int(items[2])
    spointSize = int(items[3])
    channelSize = int(items[4])
    data = []

    now = 5
    
    # 왼/오 하나의 row에 채우고 1채널로 함..
    for f in range(frameSize):
        for c in range(channelSize):
            for i in range(spointSize):
                data.append(items[now])
                now += 1
    
    channelSize = 1
    spointSize *= 2

    data = np.reshape(data, (frameSize, spointSize, channelSize))
    labelOneHot = np.zeros(defines.LABEL_SIZE)
    labelOneHot[label] = 1

    if isShowLog:
        print("Format {0} Label{1} Frame{2} SPoint{3} Channel{4}"
        .format(date, label, frameSize, spointSize, channelSize))

    return np.array(data), np.array(labelOneHot)


## return single data
def _loadDataFromFile(file, isShowLog):
    fileStream = open(file)
    fileData = fileStream.readline()

    data, label = _formatData(fileData, isShowLog)
    fileStream.close()

    return data, label
    
# return dic k:integer, v:str
def _loadLabelFile(path, isShow = True):
    f = open(path)

    labelList = { -1:'None' }
    labelList.pop(-1)

    for line in f:
        if len(line) > 3:
            tokens = line.split()
            
            number = int(tokens[0])
            name = str(tokens[1])

            labelList[number] = name

            if (isShow):
                print(str(number) + ': ' + str(name))

    return labelList

# (frame_size, 128, 128, 3)
def _loadImageFiles(dirpath, fileList, isShow):
    imgList = []

    for file in fileList:      
        img = image.load_img(dirpath + "/" + file, grayscale=True)
        array = image.img_to_array(img)
        imgList.append(array)
    
    imgNumpyArray = np.array(imgList)
    #if isShow:
        #print("imgList Length: " + str(len(imgList)))
        #print("imaNumpyArray Shape: " + str(imgNumpyArray.shape))

    return imgNumpyArray

def _comp(a, b):
    return int(a[:a.find('.')]) - int(b[:b.find('.')])

def _ROI_loadAllSamplePaths(rootfolder):
    """
    Path 읽기
    0_안녕하세요, 1_바다 ... 안의 각 샘플 폴더 모두 취합
      샘플 폴더 e.g. 1_바다/../2018-05-22_230321_kyg
    
    # arguments
      e.g. rootfolder = ../data/ConvLSTM_train      
    """

    result = []

    for labelFolder in  os.listdir(rootfolder):
        if labelFolder == 'temp':
            continue
            
        path1 = os.path.join(rootfolder, labelFolder)

        for sampleFolder in os.listdir(path1):
            path2 = os.path.join(path1, sampleFolder)
            result.append(path2)

    return result

def ROI_loadDataListAll(rootPath, isShow, isShuffle):
    '''
    rootpath = data/ConvLSTM/
    '''
    samplePathList = _ROI_loadAllSamplePaths(rootPath)

    spointList, roiSampleList, labelList = \
        _ROI_loadDataList(samplePathList, isShow)
    
    if isShuffle:
        spointList, roiSampleList, labelList = \
            shuffleDataset(spointList, roiSampleList, labelList)

    return spointList, roiSampleList, labelList

def _ROI_loadDataList(samplePathList, isShow):
    """
    샘플 폴더List 읽기
      e.g. imageSamples shape = (samples, timestep, imgshape~)
    """
    spointSamples = []
    imageSamples = []
    labelSamples = []
    
    for path in samplePathList:
        spoint, images, label = \
            ROI_loadData(path, isShow)
        spointSamples.append(spoint)
        imageSamples.append(images)
        labelSamples.append(label)
    
    spointSamples = np.array(spointSamples)
    imageSamples = np.array(imageSamples)
    labelSamples = np.array(labelSamples)

    ## 로드 결과 각 라벨 몇개씩인지 프린트
    labelCnt = [0] * defines.LABEL_SIZE
    for i in range(0, len(labelSamples)):
        labelIdx = np.argmax(labelSamples[i])
        labelCnt[labelIdx] += 1
    print(labelCnt)

    return spointSamples, imageSamples, labelSamples

def ROI_loadData(dirpath, isShow):
    """
    타임스텝 단위의 모든 데이터를 읽는다.
      디렉토리 안에 있는 left, right hand 이미지, SPoint.txt 로드

    return spointData, imageList, label
    
    # return shape

      spointData = [[f1x1, f1x2 ... f1xm], ... [fnx1 ... fnxm]]
        shape eg. (76, 76, 1); frame, spoint, channel
      imageList = [L1, L2 ... Ln, R1, R2 ... Rn]
        Lx/Rx = image raw data. eg. (128, 128, 3)
        shape eg. (100, 128, 128, 3); timestep, imgshape~
      label = [0 0 0 1 0 0]. ig. onehot
    """

    imageFileList = []
    imageList = [] # left, right sum

    # 폴더내 이미지 파일명 소트, Spoint.txt 리스트에서 제거
    for f in os.listdir(dirpath):
        if f.find('Spoints.txt') == -1:
            imageFileList.append(f)

    imageFileList.sort(key=functools.cmp_to_key(_comp))

    # 이미지 로드
    imageList = _loadImageFiles(dirpath, imageFileList, isShow)
    
    # Spint 로드
    spointData, label = _loadDataFromFile(dirpath + "/Spoints.txt", isShow)

    # 이미지 확인법
    #plt.imshow(imageList[0][0] / 255) #settingwindow
    #plt.show() #show

    return spointData, imageList, label

def ROI_loadSingleImages(dirpath, isShow):
    """
    한 장 단위의 그림을 읽어서 학습/예측하는 모델에 쓰임
      dirpath 안 파일: LabelDirs
      LabelDir 명 규칙: labelNumber_anyting
      LabelDir 안 파일: 이미지들
      
      eg.
        dirpath/0_hello/helloimg0.jpg
        dirpath/0_hello/helloimg1.bmp
        dirpath/1_loves/img.jpg
    
    return imageList, labels

    이 함수는 Convolution 모델이 제대로 작동하는지 확인하기 위해 만듦
    """
    imageList = []
    labels = []
    labelSize = 2

    # 디렉토리 서치
    dirs = os.listdir(dirpath)

    # 각 디렉트리당 이미지 로드
    for directory in dirs:
        label = int(directory.split('_')[0])
        path = dirpath + '\\' + directory
        
        images = _loadImageFiles(path, os.listdir(path), isShow)
        for image in images:
            imageList.append(image)

            labelOneHot = np.zeros(labelSize)
            labelOneHot[label] = 1
            labels.append(labelOneHot)

    imageList = np.array(imageList)
    labels = np.array(labels)

    print(imageList.shape)
    print(labels.shape)

    return imageList, labels

import numpy as np
import random
def shuffleDataset(d1, d2, d3):
    '''
    # Return
      shuffled data (d1, d2, d3)
    '''
    if len(d1) != len(d2) or len(d2) != len(d3):
        raise Exception("Lengths don't match")
    indexes = list(range(len(d1)))
    random.shuffle(indexes)
    d1_shuffled = [d1[i] for i in indexes]    
    d2_shuffled = [d2[i] for i in indexes]
    d3_shuffled = [d3[i] for i in indexes]
    return np.array(d1_shuffled), np.array(d2_shuffled), np.array(d3_shuffled)
