import sys, os
import models
import numpy as np
import dataFormater
import train
import labelDictionary as labelPy

labelDicPath = '../data/LABEL.txt'
weightPath = 'models/weights.kyg'
weightPath = dataFormater.relativePathToAbsolutePath(weightPath)
labelDicPath = dataFormater.relativePathToAbsolutePath(labelDicPath)

#load labelDic
labelDic = labelPy.loadLabelFile(labelDicPath)

#load model
print('=' * 30)
print(' Model Loading Process')
print('=' * 30)

architecture = models.getCurrentModel()
model = models.loadModel(architecture, weightPath)

#logic
print('=' * 30)
print(' Predict Process')
print('=' * 30)
while(True):
    #수신
    data = sys.stdin.readline()
    dataFomated, label = dataFormater.formatData(data, True)

    #예측
    #(76, 76, 1)을 리스트화(1, 76, 76, 1)해서 넣고
    #결과리스트로 나온것의 argmax중 [0](==0번째 데이터)을 취함
    predicted = model.predict(np.array([dataFomated]))
    
    highstIdx = np.argmax(predicted[0])
    labelName = labelDic[highstIdx]
    percent = int(predicted[0][highstIdx] * 100)
    
    #내부출력
    formatedResult = []
    for raw_result in predicted[0]:
        formattedPercent = int(raw_result * 100)
        formatedResult.append(formattedPercent)
    print(str(formatedResult) + ' -> ' + labelName)

    #결과를 메인창에 보여주기 위해[Result]접두사 추가
    resultMessage = str('[Result]') + str(labelName) + ' ' + str(percent) + '%'

    #전송
    print(resultMessage)