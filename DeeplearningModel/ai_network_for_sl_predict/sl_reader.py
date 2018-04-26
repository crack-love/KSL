import numpy as np
import os


def msg_reader(msg):
    print(len(msg))
    label_to_one_hot = {'0': [1, 0, 0, 0], '1': [0, 1, 0, 0], '2': [0, 0, 1, 0], '3': [0, 0, 0, 1]}

    data_set = []
    label_set = []

    items = msg.split()

    date = items[0]
    label = items[1]

    frame_length = int(items[2])
    data_length = int(int(items[3]) / 2)  # 왼손 오른손
    channels = int(items[4])

    total_length = int(frame_length * data_length)
    left_feature = []
    right_feature = []
    idx = 5

    print(total_length)
    print(data_length)

    for i in range(total_length):
        left = items[idx]
        idx += 1
        right = items[idx]
        idx += 1

        left_feature.append(left)
        right_feature.append(right)

    left_feature = np.array(left_feature)
    left_feature = np.reshape(left_feature, (frame_length, data_length))
    right_feature = np.array(right_feature)
    right_feature = np.reshape(right_feature, (frame_length, data_length))

    feature = []
    feature.append(left_feature)
    feature.append(right_feature)

    feature = np.array(feature)
    feature = np.swapaxes(feature, 0, 2)
    feature = np.swapaxes(feature, 0, 1)

    label_set.append(label_to_one_hot[label])
    data_set.append(feature)

    return np.array(data_set), np.array(label_set)


def file_reader(file):
    label_to_one_hot = {'0': [1, 0, 0, 0], '1': [0, 1, 0, 0], '2': [0, 0, 1, 0], '3': [0, 0, 0, 1]}

    data_set = []
    label_set = []

    f = open(file)

    for line in f:
        print(len(line))
        items = line.split()

        date = items[0]
        label = items[1]

        frame_length = int(items[2])
        data_length = int(int(items[3]) / 2)  # 왼손 오른손
        channels = int(items[4])

        total_length = int(frame_length * data_length)
        left_feature = []
        right_feature = []
        idx = 5

        for i in range(total_length):
            left = items[idx]
            idx += 1
            right = items[idx]
            idx += 1

            left_feature.append(left)
            right_feature.append(right)

        left_feature = np.array(left_feature)
        left_feature = np.reshape(left_feature, (frame_length, data_length))
        right_feature = np.array(right_feature)
        right_feature = np.reshape(right_feature, (frame_length, data_length))

        feature = []
        feature.append(left_feature)
        feature.append(right_feature)

        feature = np.array(feature)
        feature = np.swapaxes(feature, 0, 2)
        feature = np.swapaxes(feature, 0, 1)

        label_set.append(label_to_one_hot[label])
        data_set.append(feature)

    f.close()
    return np.array(data_set), np.array(label_set)


if __name__ == "__main__":
    # f = open('../data/train_data/과자/2018-04-24_154359_과자.txt')
    # msg = f.read()
    # data_set, label_set = msg_reader(msg)

    data_set, label_set = file_reader('../data/train_data/과자/2018-04-24_154359_과자.txt')
    print(data_set.shape, label_set.shape)
