import numpy as np
import random
import heapq
from . import config

tasks = []  # 任务集合，tasks[i]表示第i个任务第长度
taskNum = 100  # 任务数量

nodes = []  # 处理节点集合，nodes[i] 表示第i个节点处理速度
nodeNum = 10  # 节点数量

# 随机生成测试数据第范围
taskLengthRange = {'min': 10, 'max': 100}  # 任务长度取值范围
nodeSpeedRange = {'min': 10, 'max': 100}  # 处理速度取值范围

# 任务处理时间矩阵(记录单个任务在不同节点上的处理时间)
timeMatrix = []

iteratorNum = 100  # 迭代次数
chromosomeNum = 10  # 染色体数量

adaptability = []  # 适应度矩阵(下标：染色体编号、值：该染色体的适应度)
selectionProbability = []  # 自然选择的概率矩阵(下标：染色体编号、值：该染色体被选择的概率)

cp = 0.2  # 染色体复制的比例(每代中保留适应度较高的染色体直接成为下一代)
crossoverMutationNum = int(chromosomeNum - chromosomeNum * cp)  # 参与交叉变异的染色体数量
resultData = []  # 任务处理时间结果集([迭代次数][染色体编号])


# 从config引入参数
def checkConfig(userConfig={}):
    global taskNum, nodeNum, iteratorNum, chromosomeNum, cp, crossoverMutationNum
    if len(userConfig) == 0:
        taskNum = config.GA_CONFIG['taskNum']  # 任务数量
        nodeNum = config.GA_CONFIG['nodeNum']  # 节点数量
        iteratorNum = config.GA_CONFIG['iteratorNum']  # 迭代次数
        chromosomeNum = config.GA_CONFIG['chromosomeNum']  # 染色体数量
        cp = config.GA_CONFIG['cp']  # 染色体复制的比例(每代中保留适应度较高的染色体直接成为下一代)
        crossoverMutationNum = int(chromosomeNum - chromosomeNum * cp)  # 参与交叉变异的染色体数量
    else:
        taskNum = int(userConfig['taskNum'])  # 任务数量
        nodeNum = int(userConfig['nodeNum'])  # 节点数量
        iteratorNum = int(userConfig['iteratorNum'])  # 迭代次数
        chromosomeNum = int(userConfig['chromosomeNum'])  # 染色体数量
        cp = float(userConfig['cp'])  # 染色体复制的比例(每代中保留适应度较高的染色体直接成为下一代)
        crossoverMutationNum = int(chromosomeNum - chromosomeNum * cp)  # 参与交叉变异的染色体数量



# 生成随机数组
def random_int_list(start, stop, length):
  start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
  length = int(abs(length)) if length else 0
  random_list = []
  for i in range(length):
    random_list.append(random.randint(start, stop))
  return random_list


# 初始化任务处理时间矩阵
def initTimeMatrix(tasks, nodes, timeMatrix):
    for i in range(len(tasks)):
        time_i = []
        for j in range(len(nodes)):
            time_i.append(tasks[i]/nodes[j])
        timeMatrix.append(time_i)
    return timeMatrix


def initGA():
    global timeMatrix, tasks, nodes, resultData
    resultData = []
    tasks = random_int_list(taskLengthRange['min'], taskLengthRange['max'], taskNum)
    nodes = random_int_list(nodeSpeedRange['min'], nodeSpeedRange['max'], nodeNum)
    timeMatrix = initTimeMatrix(tasks, nodes, timeMatrix)
    # print("node:", nodes)
    # print("tasks", tasks)
    # print(timeMatrix)


# 计算所有染色体的任务处理时间
def runTaskTime(chromosomeMatrix):
    global resultData
    timeArray = []
    for chromosomeIndex in range(len(chromosomeMatrix)):
        maxLength = 0
        # print(nodes)
        for nodeIndex in range(len(nodes)):
            sumLength = 0
            for taskIndex in range(len(tasks)):
                if chromosomeMatrix[chromosomeIndex][taskIndex] == nodeIndex:
                    sumLength += timeMatrix[taskIndex][nodeIndex]
            if sumLength > maxLength:
                maxLength = sumLength
        timeArray.append(maxLength)
    # print("resultData", timeArray)
    resultData.append(timeArray)


# 轮盘赌算法，用于选择上一代中的基因
def RWS(selectionProbability):
    sum = 0
    rand = random.random()
    for i in range(len(selectionProbability)):
        sum += selectionProbability[i]
        if sum >= rand:
            return i


# 交叉
def cross(chromosomeMatrix):
    newChromosomeMatrix = []
    for chromosomeIndex in range(crossoverMutationNum):
        # 使用轮盘赌选择遗传的父母染色体基因
        chromosomeFather = chromosomeMatrix[RWS(selectionProbability)]
        chromosomeMother = chromosomeMatrix[RWS(selectionProbability)]
        # 交叉
        crossIndex = random.randint(0, taskNum - 1)
        chromosomeNew = chromosomeFather[:crossIndex] + chromosomeMother[crossIndex:]
        newChromosomeMatrix.append(chromosomeNew)
    return newChromosomeMatrix


# 变异
def mutation(newChromosomeMatrix):
    # 随机找一条染色体、一个任务、一个节点进行替换
    chromosomeIndex = random.randint(0, crossoverMutationNum - 1)
    taskIndex = random.randint(0, taskNum - 1)
    nodeIndex = random.randint(0, nodeNum - 1)
    newChromosomeMatrix[chromosomeIndex][taskIndex] = nodeIndex
    return newChromosomeMatrix


# 从数组中寻找最大的n个元素
def maxN(array, n):
    maxIndex = []
    tmparray = array
    for i in range(n):
        maxVule = max(tmparray)
        index = array.index(maxVule)
        maxIndex.append(index)
        tmparray[index] = 0    # 因为都是大于0的
    return maxIndex


# 复制
def copy(chromosomeMatrix, newChromosomeMatrix):
    # 寻找适应度最高的N条染色体的下标(N=染色体数量*复制比例)
    cpNum = int(chromosomeNum*cp)
    chromosomeIndexArr = maxN(adaptability, cpNum)
    # chromosomeIndexArr = heapq.nlargest(cpNum,adaptability)
    # 复制
    for i in range(len(chromosomeIndexArr)):
        chromosome = chromosomeMatrix[chromosomeIndexArr[i]]
        newChromosomeMatrix.append(chromosome)
    return newChromosomeMatrix


def createGeneration(chromosomeMatrix=[]):
    if len(chromosomeMatrix) == 0:  # 第一代染色体
        newChromosomeMatrix = []
        for i in range(chromosomeNum):
            chromosomeMatrix_i = []
            for j in range(taskNum):
                chromosomeMatrix_i.append(random.randint(0, nodeNum - 1))
            newChromosomeMatrix.append(chromosomeMatrix_i)
        # 计算当前染色体需要的处理时间
        # print("ChromosomeMatrix", newChromosomeMatrix)
        runTaskTime(newChromosomeMatrix)
        return newChromosomeMatrix
    else:
        # 交叉、变异、复制
        newChromosomeMatrix = cross(chromosomeMatrix)
        newChromosomeMatrix = mutation(newChromosomeMatrix)
        newChromosomeMatrix = copy(chromosomeMatrix, newChromosomeMatrix)

        runTaskTime(newChromosomeMatrix)
        return newChromosomeMatrix


# 计算染色体适应度
def calAdaptability(chromosomeMatrix):
    global adaptability
    adaptability = []
    for chromosomeIndex in range(chromosomeNum):
        maxLength = 0
        for nodeIndex in range(nodeNum):
            sumLength = 0
            for taskIndex in range(taskNum):
                if chromosomeMatrix[chromosomeIndex][taskIndex] == nodeIndex:
                    sumLength += timeMatrix[taskIndex][nodeIndex]
            if sumLength > maxLength:
                maxLength = sumLength
        adaptability.append(1/maxLength)    # 适应度 = 1/任务长度


# 计算自然选择概率
def calSelectionProbability(adaptability):
    global selectionProbability
    # print("adaptability", adaptability)
    selectionProbability = []
    # 计算适应度总和
    sumAdaptability = 0
    for i in range(chromosomeNum):
        sumAdaptability += adaptability[i]

    # 计算每条染色体的选择概率
    for i in range(chromosomeNum):
        selectionProbability.append(adaptability[i]/sumAdaptability)



def gaSearch(iteratorNum, chromosomeNum):
    # 第一代
    chromosomeMatrix = createGeneration()

    # 迭代
    for itIndex in range(1,iteratorNum):
        # print(itIndex)
        # 计算上一代各条染色体的适应度
        calAdaptability(chromosomeMatrix)
        # 计算自然选择概率
        calSelectionProbability(adaptability)
        # 生成新染色体
        chromosomeMatrix = createGeneration(chromosomeMatrix)

def main(**kwargs):
    checkConfig(**kwargs)
    # print(taskNum, nodeNum, iteratorNum, chromosomeNum, cp, crossoverMutationNum)
    initGA()
    gaSearch(iteratorNum, chromosomeNum)


# 返回结果数组
def getResultData():
    return resultData


if __name__ == "__main__":
    main()