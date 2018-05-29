import numpy as np


def calculateAccuracy(dataList, labelList, size, model, verbose, batch_size):
    '''
    print('raw predicted')
    print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))
    '''
    '''print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))
    '''
    predicted = model.predict(x=dataList, verbose=verbose, batch_size=batch_size)

    predicted_oneHot = np.argmax(predicted, 1)
    predicteShouldBeList = np.argmax(labelList, 1)

    print('Percent:')
    _printFloatViewable(predicted)
    print('Source:')
    print(predicteShouldBeList)
    print('Predicted:')
    print(predicted_oneHot)

    accuracy = np.sum(np.equal(predicted_oneHot, predicteShouldBeList)) / size

    return accuracy

def _printFloatViewable(plist):
    sampleSize=len(plist)
    labelSize=len(plist[0])
    for i in range(sampleSize):
        for j in range(labelSize):
            plist[i][j] = round(plist[i][j], 2)
    
    print(plist)