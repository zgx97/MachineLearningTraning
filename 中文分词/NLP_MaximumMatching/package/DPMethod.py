#!/usr/bin/env python
# coding=utf-8

import collections


class Words_Freq_DP():
    def __init__(self):
        self.dict = {}
        self.total_words = 0

    '''
    从词频表读取的词频数据
    defaultdic 词频表没有某个词组，就返回1，与dict.get(,default)功能相似
    '''
    def load_data(self, filename):
        self.dict = collections.defaultdict(lambda:1)
        self.total_words = 0
        data = open(filename, "r", encoding="gb18030")
        for line in data:
            word, freq = line.split('\t')[0:2]
            self.total_words += 1
            try:
                self.dict[word.decode('gbk')] = int(freq)
            except:
                self.dict[word] = int(freq)
    
    '''
    根据单词出现的频次进行dp
    '''
    def cut(self, sent):
        sent_len = len(sent)
        prb = [0 for i in range(sent_len+1)]
        prb[sent_len] = 1
        div = [1 for i in range(sent_len+1)]
        ind = [1 for i in range(sent_len)]
        
        for i in range(sent_len-1, -1, -1):
            for k in range(1, sent_len-i+1):
                if k > 1 and self.dict[sent[i:i+k]] == 1:
                    continue
                if self.dict[sent[i:i+k]] * prb[i+k] * div[i] > \
                   prb[i] * self.total_words * div[i+k]:
                    prb[i] = self.dict[sent[i:i+k]]*prb[i+k]
                    div[i] = self.total_words * div[i+k]
                    ind[i] = k
        
        sent_cut = []
        i = 0
        while i < sent_len:
            sent_cut.append(sent[i:i+ind[i]])
            i += ind[i]
        return sent_cut
    
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

