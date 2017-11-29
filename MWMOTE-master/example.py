# coding=utf-8
import pickle, MWMOTE, random, math
import matplotlib.pyplot as plt
import numpy as np
import re
import os
from collections import Counter
import toArff

# def load_data(path):
#   data_X = []
#   data_Y = []
#   with open(path, 'r') as f:
#     for line in f.readlines():
#       line = line.rstrip().split(" ")
#       data_Y.append(int(line[0]))
#       instance = [0 for i in range(14)]
#       for i in line[1:]:
#         tmp = i.split(':')
#         instance[int(tmp[0])] = float(tmp[1])
#       data_X.append(instance)

#   return (data_X,data_Y)


# def example():
#     N = 5000
#     X = []
#     Y = [1 for i in range(N)]
#
#     for i in range(N):
#         X.append([random.uniform(0, 10), random.uniform(0, 10)])
#
#     for i, j in enumerate(X):
#         if math.hypot(j[0], j[1]) < 5 or math.hypot(j[0] - 10, j[1] - 10) < 2:
#             Y[i] = -1
#         if random.random() < 0.01:
#             Y[i] = -Y[i]
#     return X, Y


class mwmote:
    def loadSample(self, filename):
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
            Y_data.append(numList[-1])
        f.close()
        return X_data, Y_data

    def write_resample(self, path, resampled):
        f = open(path, 'w')
        for i in range(len(resampled)):
            for j in range(len(resampled[i])):
                if j < len(resampled[i]) - 1:
                    f.write(str(resampled[i][j]) + ',')
                else:
                    f.write(str(resampled[i][j]))
            f.write('\n')
        f.close()
    def run_dir(self, path_original, path_saveNew,p):
        pathdir_original = os.listdir(path_original)  # 列出原始样本文件夹下的文件名和文件夹名
        for name in pathdir_original:  # 对文件名进行循环
            if os.path.isfile(path_original + "\\" + name):  # 如果name是一个文件，这里传入的路径必须是绝对路径才可以判断
                X, Y = self.loadSample(path_original + "\\" + name)  # 加载文件数据
                countDict=dict(Counter(Y))
                N=countDict[1]-countDict[0]
                MWMOTE.MWMOTE(X, Y, N)
                for k,v in enumerate(Y):
                    X[k].append(v)

                # X_resampled, y_resampled = ada.fit_sample(X, y)
                # y_resampled = y_resampled[:, np.newaxis]
                # resampled = np.hstack((X_resampled, y_resampled)).tolist()
                self.write_resample(path_saveNew + '\\for_' + str(p + 1) + '\\re_mwsmote_' + name, X)
            else:  # 如果name是一个文件夹
                path1 = path_original + "\\" + name  # 更新原始数据集路径
                if not os.path.exists(path_saveNew + "\\" + name):
                    os.mkdir(path_saveNew + "\\" + name)  # 创建和原始数据集文件夹一致的文件夹，用于保存采样的结果
                path2 = path_saveNew + "\\" + name  # 更新保存数据的路径为新创建的文件夹
                for i in range(m):  # 在这个文件夹中创建存放每一次循环采样结果的文件夹
                    if not os.path.exists(path2 + "\\for_" + str(i + 1)):
                        os.mkdir(path2 + "\\for_" + str(i + 1))
                self.run_dir(path1, path2,p)  # 调用循环采样的方法，循环调用



if __name__ == '__main__':
    # with open('./heart_scale.pickle', 'r') as f:
    #   X,Y = pickle.load(f)
    pathOriginal="C:\\Users\\Administrator\\Desktop\\Original_dataset20171121"
    pathsaveNew="C:\\Users\\Administrator\\Desktop\\test_dic"
    pathsaveNewArff="C:\\Users\\Administrator\\Desktop\\test_dic_arff"
    mw=mwmote()
    m=10
    for p in range(m):
        mw.run_dir(pathOriginal,pathsaveNew,p)
    toArff.run_dir(pathsaveNew,pathsaveNewArff)
    # X, Y = example()
    #
    # X_p = []
    # X_n = []
    # for i, j in enumerate(Y):
    #     if j == -1:
    #         X_n.append(X[i])
    #     else:
    #         X_p.append(X[i])
    #
    # x = np.array(X_p)
    # y = np.array(X_n)
    #
    # plt.plot(x[:, 0], x[:, 1], 'og', ms=5)
    # plt.plot(y[:, 0], y[:, 1], 'ob', ms=5)
    #
    # X_g, Y_g = MWMOTE.MWMOTE(X, Y, 1000)
    # z = np.array(X_g)
    # plt.plot(z[:, 0], z[:, 1], 'or', ms=5)
    # plt.show()
