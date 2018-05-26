import numpy as np

def calculateAccuracy(dataList, labelList, size, model, verbose, batch_size):
    '''
    print('raw predicted')
    print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))
    '''
    '''print(model.predict(x=dataList, verbose=verbose, batch_size=batch_size))
    '''
    predicted = model.predict(x=dataList, verbose=verbose, batch_size=batch_size)
    predicted_fit = np.argmax(predicted, 1)
    predicteShouldBeList = np.argmax(labelList, 1)

    print(predicted)
    print('Source:')
    print(predicteShouldBeList)
    print('Predicted:')
    print(predicted_fit)

    accuracy = np.sum(np.equal(predicted_fit, predicteShouldBeList)) / size

    return accuracy