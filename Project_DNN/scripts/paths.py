import os
import interfaceUtils as utils

''' ---------------------------------------------------

PATH 제공, 스크립트:
relative path를 하드코드로 가지고 있다가 런타임에
absolute path로 변경하여 Dictionary 형태로 제공한다
(absolute path를 제공)

0. absolute 변환 시 PATH 존재 여부 확인하여 에러 출력
1. relative 기준은 이 스크립트 위치
2. key는 대소문자 구별 없음

--------------------------------------------------- '''

_DIC = { }

def relToAb(rel):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return dirpath + "\\" + rel

def append(key, val):
    _DIC[key.upper()] = val

def get(key):
    return _DIC[key.upper()]

def init():
    print('Using modified Paths.')
    
    append('label', '..\\..\\data\\LABEL.txt')
    append('weight', '..\\models\\weights.keras')
    append('train', '..\\..\\data\\train')
    append('test', '..\\..\\data\\test')

    # Change relative to absolute
    # Error File/Folder is not exist
    for key in _DIC:
        _DIC[key] = relToAb(_DIC[key])

        # Path 미존재
        if (os.path.exists(_DIC[key]) == False):
            utils.showError('{0} 파일/폴더를 찾을 수 없습니다.'.format(_DIC[key]))
        #else:
            #print(key + ": OK")

init()