

def loadLabelFile(path):
    f = open(path)

    labelList = { -1:'None' }

    for line in f:
        if len(line) > 3:
            tokens = line.split()
            
            number = int(tokens[0])
            name = str(tokens[1])

            labelList[number] = name

            print(str(number) + ': ' + str(name))

    return labelList