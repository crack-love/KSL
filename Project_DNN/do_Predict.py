import PYTHONPATH
import sys, os
import numpy as np
import scripts.models as models
import scripts.dataFormater as DFormat
import scripts.interfaceUtils as utils
from scripts.Path import Path

#load labelDic
utils.showProcess('Label Loading Process')
labelDic = DFormat._loadLabelFile(Path.get('label'))

#load model
utils.showProcess('Model Loading Process')
model = models.Model_M1_Self()
models.loadWeight(model, Path.get('weight'))

#logic
utils.showProcess('Predict Process')
while (True):
    # 수신
    data = sys.stdin.readline()
    if str(data).find('[Predict]') is -1:
        continue
    
    spointData, imageList, label = \
        DFormat.ROI_loadData(Path.get('temp'), True)

    spointData = np.array([spointData])
    imageList = np.array([imageList])
    label = np.array([label])
    #print(spointData.shape)
    #print(imageList.shape)

    # 예측
    # (150, 74, 1)을 리스트로 wrap(1, 150, 74, 1)해서 넣고
    # 결과리스트로 나온것 중 0번째 데이터를 취함
    # 참고로 keras놈은 모든 에레이를 np.array로 wrap해야 함 (변화는 없음)
    predicted = model.predict([spointData, imageList])

    # 퍼센트 
    highstIdx = np.argmax(predicted[0])
    believe = int(predicted[0][highstIdx] * 100) # 신뢰율

    # 내부출력 (each labels percent)
    allresult = []
    for each_result in predicted[0]:
        each_percent = int(each_result * 100)
        allresult.append(each_percent)
    
    labelName = labelDic[highstIdx]
    print(str(allresult) + ' -> ' + labelName)

    # 결과를 메인창에 보여주기 위해[Result]접두사 추가
    resultMessage = str('[Result]') + str(labelName) + ' ' + str(believe) + '%'

    # 전송
    print(resultMessage)