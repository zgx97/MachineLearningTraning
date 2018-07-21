#!/usr/bin/env python
# coding=utf-8

from .extra import get_word_maxlen

'''
    反向最大匹配算法：
        原理： 与正向最大匹配算法相同
        优化： 同样与 FMM 相似，可以优化寻找最大后缀效率
'''
class BMM():
    def __init__(self):
        self.words_dict = {}
        self.words_mlen = 0
        self.init_flag = False

    def set_up(self):
        self.init_flag = True 

    def load_dict(self, filename):
        self.words_mlen = 5
        dict_data = open(filename, "r", encoding="gb18030")
        for word in dict_data:
            word = word.strip('\n')
            self.words_dict[word] = 1

    def cut(self, observe):
        sent_cut = []
        obs_len = len(observe)
        i = obs_len - 1
        while i >= 0:
            start_ind = 0
            if i - self.words_mlen + 1 >= 0:
                start_ind = i - self.words_mlen + 1

            word = observe[start_ind:i+1]
            while self.words_dict.get(word, 0) == 0:
                word = word[1:len(word)+1]
                if len(word) == 1 or len(word) == 0:
                    break
            if len(word) == 0:
                break
            sent_cut.append(word)
            i = i - len(word)
        return [sent_cut[len(sent_cut) - 1 - i] for i in range(len(sent_cut))]

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





    
