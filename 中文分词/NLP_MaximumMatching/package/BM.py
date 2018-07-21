#!/usr/bin/env python
# coding=utf-8

'''
    双向最大匹配法
    1.如果正反向分词结果词数不同，则取分词数量较少的那个。
    2.如果分词结果词数相同
        a.分词结果相同，就说明没有歧义，可返回任意一个。
        b.分词结果不同，返回其中单字较少的那个。
'''

from .FMM import FMM 
from .BMM import BMM 
from .extra import get_word_maxlen

class BM():
    def __init__(self):
        self.words_dict = {}
        self.words_mlen = 0
        self.fmm = FMM()
        self.bmm = BMM() 

    def load_dict(self, filename):
        self.fmm.load_dict(filename)
        self.bmm.load_dict(filename)

    def cut(self, observe):
        ret1 = self.fmm.cut(observe)
        ret2 = self.bmm.cut(observe)

        if len(ret1) == 0:
            return ret2 
        if len(ret2) == 0:
            return ret1

        if ret1 == ret2:
            return ret1 
        else:
            if len(ret1) < len(ret2):
                return ret1
            else:
                return ret2

    def test(self, testfile, outfile):
        cases = open(testfile, "r", encoding="gb18030")
        fw = open(outfile, "w", encoding="gb18030") 
        for case in cases:
            result = self.cut(case.strip().strip("\n"))
            writeStr = ""
            for word in result:
                writeStr = writeStr + str(word) + " "
            fw.write(writeStr.strip(" ")+"\n")
        cases.close()
        fw.close()          





    
