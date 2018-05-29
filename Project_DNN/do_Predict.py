import PYTHONPATH
import sys, os
import numpy as np
import scripts.models as models
import scripts.dataFormater as DFormat
import scripts.interfaceUtils as utils
import scripts.paths as PATH

labelDicPath = PATH.get('label')
weightPath = PATH.get('weight')

#load labelDic
utils.showProcess('Label Loading Process')
labelDic = DFormat.loadLabelFile(labelDicPath)

#load model
utils.showProcess('Model Loading Process')
model = models.loadModel(weightPath)

#logic
utils.showProcess('Predict Process')
while (True):

    # 수신
    data = sys.stdin.readline()  # C#에서 WriteLine을 통해 입력한 데이터를 읽음
    dataFomated, label = DFormat.formatData(data, True)  # 읽어온 데이터를 모델에 넣을 수 있도록 포맷팅

    # 예측
    # (76, 76, 1)을 리스트로 wrap(1, 76, 76, 1)해서 넣고
    # 결과리스트로 나온것 중 0번째 데이터를 취함
    # 참고로 keras놈은 모든 에레이를 np.array로 wrap해야 함 (변화는 없음)
    predicted = model.predict(np.array([dataFomated]))
    
    highstIdx = np.argmax(predicted[0])
    labelName = labelDic[highstIdx]
    believe = int(predicted[0][highstIdx] * 100) # 신뢰율
    
    # 내부출력 (each labels percent)
    allresult = []
    for each_result in predicted[0]:
        each_percent = int(each_result * 100)
        allresult.append(each_percent)

    print(str(allresult) + ' -> ' + labelName)

    # 결과를 메인창에 보여주기 위해[Result]접두사 추가. C#에서 Login 클래스에서 출력값을 받았을 때 [Result]가 앞에 붙어 있을 경우 form의 labelMain에 출력
    resultMessage = str('[Result]') + str(labelName) + ' ' + str(believe) + '%'

    # 전송
    print(resultMessage)