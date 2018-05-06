import os, sys
import train
import models
import dataFormater as formatter
import tensorflow as tf

trainDataFolderPath = '../data/train'
testDataFolderPath = '../data/test'
weightScriptRelativePath = 'models/weights.kyg'

# Print Device
'''
print('-' * 30)
print(' Device')
print('-' * 30)
sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
'''

print('How many epoch ? ')
response = sys.stdin.readline().strip()
epoch = int(response)

# path: relative to absolute
trainDataFolderPath = formatter.relativePathToAbsolutePath(trainDataFolderPath)
testDataFolderPath = formatter.relativePathToAbsolutePath(testDataFolderPath)
weightScriptRelativePath = formatter.relativePathToAbsolutePath(weightScriptRelativePath)

print('-' * 30)
print(' Loding Previous model')
print('-' * 30)

# load model
architecture = models.getCurrentModel()
model = models.loadModel(architecture, weightScriptRelativePath)
model = architecture

print('-' * 30)
print(' Loding Data')
print('-' * 30)

# load data
# 2nd argument(Bool) mean show log to stdout
trainDatas, trainLabels = formatter.loadDataFromDir(trainDataFolderPath, True)    
testDatas, testLabels = formatter.loadDataFromDir(testDataFolderPath, True)

print('-' * 30)
print(' Train Start')
print('-' * 30)   

# train
train.train(trainDatas, trainLabels, model, epoch, 32)

print('-' * 30)
print(' Evaluate Accuracy')
print('-' * 30)
 
accuracy = train.calculateAccuracy(trainDatas, trainLabels, model)
print("Accuracy train: " + str(accuracy))
accuracy = train.calculateAccuracy(testDatas, testLabels, model)
print("Accuracy test: " + str(accuracy))

print('-' * 30)
print(' Save Model')
print('-' * 30)

# save
print(weightScriptRelativePath)
models.saveModel(model, weightScriptRelativePath)
print('Complete')