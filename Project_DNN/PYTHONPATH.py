# ---------------------------------------------------
# 
# 필수 import 파일임:
# scripts 폴더의 스크립트들이 서로 import하기 위해서는
# scripts 폴더를 pythonpath에 등록해야한다.
# 
# ---------------------------------------------------

import os

dirpath = os.path.dirname(os.path.realpath(__file__))
dirpath = dirpath + "\\scripts"

print('Using modified Pythonpath from PYTHONPATH.py')

os.sys.path.append(dirpath)