import numpy as np

def calculateAccuracy(dataList, labelList, model, verbose):
    
    size = len(dataList)

    predictedList = np.argmax(model.predict(x=dataList, verbose=verbose), 1)
    predicteShouldBeList = np.argmax(labelList, 1)

    accuracy = np.sum(np.equal(predictedList, predicteShouldBeList)) / size

    return accuracy

def train(trainDatas, trainLabels, model, epoch, batch):

    # Training
    # verbose 보여주는형식
    model.fit(trainDatas, trainLabels, batch_size=batch, epochs=epoch, verbose=1, shuffle=True)