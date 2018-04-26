import ai_network_for_sl_predict.sl_reader as io
import socket
import models
import numpy as np


if __name__ == '__main__':
    model = models.sl_model_for_new_data()
    # model.load_weights('../../weights.h5')
    # model.load_weights('weights.h5')
    # model.load_weights('../../weights_new.h5')
    model.load_weights('../weights_new.h5')

    ip = '127.0.0.1'
    port = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(0)

    print("deeplearning server running!")
    while True:
        client_socket, addr = server_socket.accept()  # 클라이언트가 연결될 때까지 기다립니다.
        print("accept client!")
        # msg = client_socket.recv(65535).decode("utf-8")
        # print(msg)

        # data, label = io.msg_reader(msg)
        data, label = io.file_reader("../../Project_Kinect/temp.txt")
        try:
            prediction = model.predict(data)

            client_socket.send(str(np.argmax(prediction[0])).encode("utf-8"))
            print(np.argmax(prediction[0]))

        except:
            print("error occured!")

        client_socket.close()

    server_socket.close()

    # print(predict)
