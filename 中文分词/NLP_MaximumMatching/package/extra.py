#!/usr/bin/env python
# coding=utf-8

'''
get_word_maxlen : 得到词典中最长的长度，以此来确定FMM，BMM的最大长度
'''
def get_word_maxlen(filename):
    fr = open(filename, "r", encoding="gb18030")
    maxlens  = 0
    for line in fr:
        maxlens = max(maxlens, len(line))
    return maxlens

'''
get_largest_word : 在字典中找到word的最大前缀
'''
def get_largest_word(word, dict):
    while word not in dict:
        word = word[:len(word)-1]
        if len(word) == 1 or len(word) == 0:
            break
    return word