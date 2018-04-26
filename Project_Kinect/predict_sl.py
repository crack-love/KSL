import argparse
import sl_reader
import models
import numpy as np


if __name__ == '__main__':
    """
    parser = argparse.ArgumentParser()
    parser.parse_args()
    parser.add_argument('x', type=str, help="input file name")
    args = parser.parse_args()

    file = args.x
    print(file)
    """

    # data = sl_reader.file_reader(file)

    # model = models.sl_model()
    # model.load_weights('weights.h5')

    #predict = model.predict(model)

    #predict_arg_max = np.argmax(predict, axis=1)

    #print(predict)
    #print(data)

    parser = argparse.ArgumentParser()
    parser.add_argument('read', type=str,
                        help="input read file name")
    parser.add_argument('write', type=str,
                        help="input write file name")
    args = parser.parse_args()

    read = args.read

    data = sl_reader.file_reader_for_new(read)
    # data = sl_reader.file_reader('data/바다(test).txt')
    # data2 = sl_reader.file_reader('data/안녕하세요(test).txt')

    # data = np.concatenate((data, data2))
    # model = models.sl_model()
    model = models.sl_model_for_new_data()
    # model.load_weights('../../weights.h5')
    # model.load_weights('weights.h5')
    model.load_weights('weights_new.h5')

    try:
        predict = model.predict(data)
        # print(predict)

        # predict = model.predict(data2)
        # print(predict)
        # print(predict[0])

        f = open(args.write, 'w')
        f.write(str(np.argmax(predict[0])))

    except:
        print("error occured!")
    # print(predict)
