import PYTHONPATH
import tensorflow as tf
import scripts.interfaceUtils as util
import scripts.models as models
import scripts.dataFormater as DFormat
import scripts.train as train
import scripts.paths as path

BATCH_SIZE = 32

# input epochs
util.showDivisionSingle()
epoch = int(util.input('How many epochs?'))

# load path
trainDataPath = path.get('TRAIN')
testDataPath = path.get('TEST')
weightPath = path.get('WEIGHT')

# load model
util.showProcess('Loading Previous model')
model = models.loadModel(weightPath)

# load data
util.showProcess('Loading Data')
trainDatas, trainLabels = DFormat.loadDataFromDir(trainDataPath, False)    
testDatas, testLabels = DFormat.loadDataFromDir(testDataPath, False)

# train
util.showProcess('Train Start')
print('BATCH_SIZE: ' + str(BATCH_SIZE))
train.train(trainDatas, trainLabels, model, epoch, BATCH_SIZE)

# result
print('Evaluate Accuracy')
accuracy = train.calculateAccuracy(trainDatas, trainLabels, model, 0)
print("Accuracy TRAIN: " + str(accuracy))
accuracy = train.calculateAccuracy(testDatas, testLabels, model, 0)
print("Accuracy TEST: " + str(accuracy))

# save
util.showProcess('Saving Weight')
models.saveModel(model, weightPath)

print('Complete')