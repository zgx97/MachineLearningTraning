#!/usr/bin/env python
# coding=utf-8

from numpy import *
import operator

import matplotlib
import matplotlib.pyplot as plt


def output(strname, tobject):
    print strname
    print tobject
    pass 

# kNN, inX输入向量, 训练样本集， 标签向量
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = dataSet - tile(inX, (dataSetSize, 1))
    sqDiffMat = diffMat ** 2
    sqDiffMat = sqDiffMat.sum(axis=1)
    distances = sqDiffMat ** 0.5
    sortedDisitIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDisitIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def file2matrix(filename):
    fr = open(filename)
    arraryOLines = fr.readlines()
    numberOfLines = len(arraryOLines)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arraryOLines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector

def drawing(datingDataMat, datingLabels, ind1, ind2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:, ind1], datingDataMat[:, ind2],
               15.0*array(datingLabels), 15.0*array(datingLabels))
    plt.show()

# 归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals

    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    # minVals是一个一维列表
    normDataSet = dataSet - tile(minVals, (m, 1)) 

    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals

def datingClassTest():
    hoRatio = 0.05
    datingDataMat, datingLabels = file2matrix("/home/zgx/Document/GitHub/MachineLearningTraning/Chapter2/DataSet/datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :], \
                datingLabels[numTestVecs:m], 2)  
        print "the classifier came back with: %d, the real answer is: %d"\
                % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))

def classifyPersin():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles  = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat, datingLabels = file2matrix("/home/zgx/Document/GitHub/MachineLearningTraning/Chapter2/DataSet/datingTestSet2.txt") 
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0(inArr, datingDataMat, datingLabels, 3)
    print "You will probably like this person: ", \
            resultList[classifierResult - 1]


if __name__ == "__main__":
    datingDataMat, datingLabels = file2matrix("/home/zgx/Document/GitHub/MachineLearningTraning/Chapter2/DataSet/datingTestSet2.txt")
    # drawing(datingDataMat, datingLabels, 0, 1)
    # drawing(datingDataMat, datingLabels, 1, 2)
    # drawing(datingDataMat, datingLabels, 0, 2)
    normDataSet, ranges, minVals = autoNorm(datingDataMat)
    datingClassTest()
    classifyPersin()