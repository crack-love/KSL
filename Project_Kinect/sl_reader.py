import numpy as np
import os


def dir_list_reader(dir_list):
    data_set = []
    label_set = []

    for dir in dir_list:
        files = os.listdir(dir)
        data_list, label_list = files_in_dir_reader(dir, files)
        data_set += data_list
        label_set += label_list

    return np.array(data_set), np.array(label_set)


def files_in_dir_reader(dir_name, files):
    # label_to_one_hot = {'안녕하세요': [1, 0], '바다': [0, 1]}
    label_to_one_hot = {'0': [1, 0, 0, 0], '1': [0, 1, 0, 0], '2': [0, 0, 1, 0], '3': [0, 0, 0, 1]}

    data_set = []
    label_set = []
    for file in files:
        f = open(os.path.join(dir_name, file))

        for line in f:
            items = line.split()

            date = items[0]
            label = items[1]

            frame_length = int(items[2])
            data_length = int(items[3])
            # channels = data_length
            # channels = int(data_length / 2)
            channels = int(items[4])

            total_length = int(frame_length * data_length / 2)
            left_feature = []
            right_feature = []
            idx = 5

            # print(total_length)
            for i in range(total_length):
                left = items[idx]
                idx += 1
                right = items[idx]
                idx += 1

                left_feature.append(left)
                right_feature.append(right)

            left_feature = np.array(left_feature)
            left_feature = np.reshape(left_feature, (frame_length, int(data_length / 2)))
            right_feature = np.array(right_feature)
            right_feature = np.reshape(right_feature, (frame_length, int(data_length / 2)))

            feature = []
            feature.append(left_feature)
            feature.append(right_feature)

            feature = np.array(feature)
            feature = np.swapaxes(feature, 0, 2)
            feature = np.swapaxes(feature, 0, 1)

            print(feature.shape)

            data_set.append(feature)
            label_set.append(label_to_one_hot[label])
        # end for line in f
        f.close()

    return data_set, label_set


def file_reader_for_new(file):
    data_set = []
    f = open(file)

    for line in f:
        items = line.split()

        date = items[0]
        label = items[1]

        frame_length = int(items[2])
        data_length = int(items[3])
        channels = int(items[4])

        total_length = int(frame_length * data_length / 2)
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
        left_feature = np.reshape(left_feature, (frame_length, int(data_length / 2)))
        right_feature = np.array(right_feature)
        right_feature = np.reshape(right_feature, (frame_length, int(data_length / 2)))

        feature = []
        feature.append(left_feature)
        feature.append(right_feature)

        feature = np.array(feature)
        feature = np.swapaxes(feature, 0, 2)
        feature = np.swapaxes(feature, 0, 1)

        data_set.append(feature)

    f.close()
    return np.array(data_set)


def files_reader(files):
    label_to_one_hot = {'안녕하세요': [1, 0], '바다': [0, 1]}

    data_set = []
    label_set = []
    for file in files:
        f = open(file)

        for line in f:
            items = line.split()

            date = items[0]
            label = items[1]

            frame_length = int(items[2])
            data_length = int(items[3])
            channels = int(items[4])

            total_length = frame_length * data_length
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

            data_set.append(feature)
            label_set.append(label_to_one_hot[label])
        # end for line in f
        f.close()

    return np.array(data_set), np.array(label_set)


def files_reader(files):
    label_to_one_hot = {'안녕하세요': [1, 0], '바다': [0, 1]}

    data_set = []
    label_set = []
    for file in files:
        f = open(file)

        for line in f:
            items = line.split()

            date = items[0]
            label = items[1]

            frame_length = int(items[2])
            data_length = int(items[3])
            channels = int(items[4])

            total_length = frame_length * data_length
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

            data_set.append(feature)
            label_set.append(label_to_one_hot[label])
        # end for line in f
        f.close()

    return np.array(data_set), np.array(label_set)


def file_reader(file):
    data_set = []
    f = open(file)

    for line in f:
        items = line.split()

        date = items[0]
        label = items[1]

        frame_length = int(items[2])
        data_length = int(items[3])
        channels = int(items[4])

        total_length = frame_length * data_length
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

        data_set.append(feature)

    f.close()
    return np.array(data_set)


if __name__ == "__main__":
    # data_set, label_set = files_reader(['data/바다(test).txt'])

    # print(data_set)
    # print(label_set)
    data_set, label_set = dir_list_reader(['data/train_data/과자', 'data/train_data/말하다', 'data/train_data/멍청하다', 'data/train_data/창의적'])
