import numpy as np

def calculateAccuracy(dataList, labelList, size, model, verbose, batch_size):
    '''
    print('raw predicted')
    print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))
    '''
    print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))

    predictedList = np.argmax(model.predict(x=dataList, verbose=verbose, batch_size=batch_size), 1)
    predicteShouldBeList = np.argmax(labelList, 1)

    print('Source:')
    print(predicteShouldBeList)
    print('Predicted:')
    print(predictedList)

    accuracy = np.sum(np.equal(predictedList, predicteShouldBeList)) / size

    return accuracy
    
def train(trainDatas, trainLabels, model, epoch, batch):

    # Training
    # verbose 보여주는형식
    model.fit(trainDatas, trainLabels, batch_size=batch, epochs=epoch, verbose=1, shuffle=True)