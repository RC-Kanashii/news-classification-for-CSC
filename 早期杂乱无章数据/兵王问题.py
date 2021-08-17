import pandas as pd
from libsvm.svmutil import *

# 读取数据
data = pd.read_csv('krkopt.data', header=None)
data.dropna(inplace=True)

# 将样本数值化
for i in [0, 2, 4]:
    data.loc[data[i] == 'a', i] = 1
    data.loc[data[i] == 'b', i] = 2
    data.loc[data[i] == 'c', i] = 3
    data.loc[data[i] == 'd', i] = 4
    data.loc[data[i] == 'e', i] = 5
    data.loc[data[i] == 'f', i] = 6
    data.loc[data[i] == 'g', i] = 7
    data.loc[data[i] == 'h', i] = 8

# 将标签数值化
data.loc[data[6] != 'draw', 6] = -1
data.loc[data[6] == 'draw', 6] = 1

# 归一化处理
for i in range(6): # 排除最后的标签
    data[i] = (data[i] - data[i].mean()) / data[i].std()

# 打乱数据集
data = data.sample(frac=1).reset_index(drop=True)
# print(data.iloc[0])

# 获得训练集和测试集
sizeOfTraining = 5000
xTraining = []
yTraining = []
for i in range(0,sizeOfTraining):
    xTraining.append(data.iloc[i])
    yTraining.append()