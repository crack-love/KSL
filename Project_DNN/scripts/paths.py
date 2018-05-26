import os
import interfaceUtils as utils

''' ---------------------------------------------------

PATH 제공, 스크립트:
relative path를 하드코드로 가지고 있다가 런타임에
absolute path로 변경하여 Dictionary 형태로 제공한다
(paths.get()으로 absolute path를 제공)

0. init 시 PATH 존재 여부 확인하여 에러 출력
1. relative 기준은 이 스크립트 위치
2. key는 대소문자 구별 없음

--------------------------------------------------- '''

_DIC = { }

def _relToAb(rel):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    return dirpath + "\\" + rel

def _append(key, val):
    _DIC[key.upper()] = val

def get(key):
    return _DIC[key.upper()]

def _init():
    print('Using preset Paths from paths.py')
    
    _append('label', '..\\..\\data\\LABEL.txt')
    #_append('weight', '..\\models\\weights.keras')
    #_append('train', '..\\..\\data\\train')
    #_append('test', '..\\..\\data\\test')
    _append('data', '..\\..\\data')
    _append('weight', '..\\weight')
    _append('img', '..\\img')

    # Change relative to absolute
    # Error File/Folder is not exist
    for key in _DIC:
        _DIC[key] = _relToAb(_DIC[key])

        # Path 미존재
        if (os.path.exists(_DIC[key]) == False):
            utils.showError('{0} 파일/폴더를 찾을 수 없습니다.'.format(_DIC[key]))
        #else:
            #print(key + ": OK")

#임포트 하자마자 초기화함
_init()