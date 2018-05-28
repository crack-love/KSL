''' ---------------------------------------------------

PATH 제공, 스크립트:
relative path를 하드코드로 가지고 있다가 런타임에
absolute path로 변경하여 Dictionary 형태로 제공한다
(Path.get()으로 absolute path를 제공)

0. init 시 PATH 존재 여부 확인하여 에러 출력
1. relative 기준은 이 스크립트 위치
2. key는 대소문자 구별 없음

--------------------------------------------------- '''

import os
import interfaceUtils as utils

class _Path():
    __DIC = { }

    def __init__(self):
        self.__append('label', '..\\..\\data\\LABEL.txt')
        self.__append('train', '..\\..\\data\\ConvLSTM_train')
        self.__append('test', '..\\..\\data\\ConvLSTM_test')
        self.__append('data', '..\\..\\data')
        self.__append('weight', '..\\weight')
        self.__append('img', '..\\img')
        self.__append('temp', '..\\..\\data\\temp')

        # Change relative to absolute
        # Error File/Folder is not exist
        for key in self.__DIC:
            self.__DIC[key] = self.__relToAb(self.__DIC[key])

            # Path 미존재
            if (os.path.exists(self.__DIC[key]) == False):
                utils.showError('{0} 파일/폴더를 찾을 수 없습니다.'.format(_DIC[key]))
            #else:
                #print(key + ": OK")

    def __relToAb(self, rel):
        dirpath = os.path.dirname(os.path.realpath(__file__))
        return dirpath + "\\" + rel

    def __append(self, key, val):
        self.__DIC[key.upper()] = val

    def get(self, key):
        return self.__DIC[key.upper()]

    def ifNoDirThanMakeDir(self, key):
        path = self.get(key)
        if not os.path.exists(path):
            os.mkdir(path)

Path = _Path()