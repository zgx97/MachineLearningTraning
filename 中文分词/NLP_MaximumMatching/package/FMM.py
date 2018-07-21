#!/usr/bin/env python
# coding=utf-8

from .extra import get_word_maxlen
from .extra import get_largest_word

'''
    正向最大匹配：
        原理 ： 在最大匹配限度之内尽可能大的匹配在字典中出现的前缀  
        优化 ： 使用Trie优化查询最大前缀过程
'''
class FMM():
    
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
    '''
    在切词这里还能进行优化，在dict中查找word的某个前缀时，可以记录一下之前
    在trie树中访问过的最长前缀，因此每次最多查询一个words_mlen即可
    '''
    def cut(self, observe, _method=get_largest_word):
        sent_cut = []
        obs_len = len(observe)
        i = 0
        while i < obs_len:
            end_ind = obs_len
            if i + self.words_mlen < obs_len:
                end_ind = i + self.words_mlen

            word = observe[i:end_ind]
            word = get_largest_word(word, self.words_dict)
            if len(word) == 0:
                break
            sent_cut.append(word)
            i = i + len(word)
        return sent_cut

    def test(self, testfile, outfile, _method=get_largest_word):
        cases = open(testfile, "r", encoding="gb18030")
        fw = open(outfile, "w", encoding="gb18030") 
        for case in cases:
            result = self.cut(case.strip().strip("\n"), _method)
            writeStr = ""
            for word in result:
                writeStr = writeStr + str(word) + " "
            fw.write(writeStr.strip(" ")+"\n")
        cases.close()
        fw.close()           





    
