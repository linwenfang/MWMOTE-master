#coding=utf-8
import re
from collections import Counter
import MWMOTE

def loadSample(filename):
    f = open(filename, 'r')  # 打开文件
    inData = f.readlines()  # 读取文件数据，以列表形式返回
    # dataSet = list()  # 用于存储格式化之后的数据
    X_data = list()
    Y_data = list()
    for line in inData:
        line = line.strip()  # 将line开头和结尾的空行去掉
        strList = re.split(r'[\s,\t]+', line)  # strList为返回的列表,列表中的元素为str类型
        '''将strList中的str类型的元素转换为float类型，方便计算'''
        numList = list()
        for item in strList:
            num = float(item)
            numList.append(num)
        X_data.append(numList[:-1])
        Y_data.append(int(numList[-1]))
    f.close()
    return X_data, Y_data
if __name__ == '__main__':
    path="C:\Users\Administrator\Desktop\OriginalDataSet\EasyEnsemble\\Balance_0_B.csv"
    X, Y = loadSample(path)  # 加载文件数据
    countDict = dict(Counter(Y))
    N = countDict[1] - countDict[0]
    try:
        X_gen, Y_gen=MWMOTE.MWMOTE(X, Y, N)
    except :
        print path