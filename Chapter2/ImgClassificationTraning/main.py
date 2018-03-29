#!/usr/bin/env python
# coding=utf-8

from KNN import *
import matplotlib
import matplotlib.pyplot as plt 

rangeCount = 20
def drawing():
    fp = open("./log.txt", "r")
    
    arrayOLines = fp.readlines()
    print arrayOLines
    arrayKNum = [(x + 1) for x in range(rangeCount)]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(arrayKNum[:], arrayOLines[:])
    plt.show() 

    fp.close()

if __name__ == "__main__":
    # for i in range(rangeCount):
    #     sugerHandWritingClassTest(i + 1)
    drawing()