import numpy as np
from keras.callbacks import ModelCheckpoint

import models
import sl_reader


if __name__ == "__main__":
    #try:
        # model = models.sl_model()
        model = models.sl_model_for_new_data()

        print('-' * 30)
        print(' Loding Train Image Set')
        print('-' * 30)

        # previous data
        # train_feature, train_result = sl_reader.files_reader(['data/바다(train).txt', 'data/안녕하세요(train).txt'])
        # test_feature, test_result = sl_reader.files_reader(['data/바다(test).txt', 'data/안녕하세요(test).txt'])

        # new data
        train_feature, train_result = sl_reader.dir_list_reader(
            ['data/train_data/과자', 'data/train_data/말하다', 'data/train_data/멍청하다', 'data/train_data/창의적'])
        test_feature, test_result = sl_reader.dir_list_reader(
            ['data/test_data/과자', 'data/test_data/말하다', 'data/test_data/멍청하다', 'data/test_data/창의적'])

        print(test_result)

        model_checkpoint = ModelCheckpoint('weights.h5', monitor='val_loss', save_best_only=True)

        model.fit(train_feature, train_result, batch_size=4, epochs=50, verbose=1, shuffle=True, callbacks=[model_checkpoint])
        model.save_weights('weights_new.h5')

        print('-' * 30)
        print(' Run Model')
        print('-' * 30)
        predict_result = model.predict(test_feature)

        print('-' * 30)
        print(' Evaluate Accuracy')
        print('-' * 30)
        test_arg_max = np.argmax(test_result, axis=1)
        predict_arg_max = np.argmax(predict_result, axis=1)

        total_len = test_result.shape[0]
        accuracy = np.sum(np.equal(test_arg_max, predict_arg_max)) / total_len
        print("accuracy: " + str(accuracy))

    #except:
    #    print("error occured!")

