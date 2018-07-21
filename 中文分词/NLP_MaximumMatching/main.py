#!/usr/bin/env python
# coding=utf-8

from package.extra import get_word_maxlen
from package.FMM import FMM 
from package.BMM import BMM
from package.BM  import BM 
from package.Trie import Trie
from package.DPMethod import Words_Freq_DP
import time

'''
显示测试信息
'''
def show_sent_info(test_model, test_type, sent="众里寻他千百度，蓦然回首，那人却在灯火阑珊处。"):
    sent_predict = test_model.cut(sent)
    print(test_type, " => ", sent_predict)

'''
FMM算法：前向最大匹配
'''
def FMM_test(wordsfile, testfile, outfile):
    fmmsegger = BMM()
    fmmsegger.load_dict(wordsfile)
    show_sent_info(fmmsegger, "FMM")
    
    starttime = time.clock()
    fmmsegger.test(testfile, outfile)
    return time.clock() - starttime

'''
BMM算法：后向最大匹配
'''
def BMM_test(wordsfile, testfile, outfile):
    bmmsegger = BMM()
    bmmsegger.load_dict(wordsfile)
    show_sent_info(bmmsegger, "BMM")
    
    starttime = time.clock()
    bmmsegger.test(testfile, outfile)
    return time.clock() - starttime

'''
BM算法：利用前向最大匹配和后向最大匹配结果启发式判断
'''
def BM_test(wordsfile, testfile, outfile):
    bmsegger = BM()
    bmsegger.load_dict(wordsfile)
    show_sent_info(bmsegger, "BM")
    
    starttime = time.clock()
    bmsegger.test(testfile, outfile)
    return time.clock() - starttime

'''
普通Ｔrie + FMM算法:先建立Trie，优化FM算法查询
'''
def Trie_FMM_test(wordsfile, testfile, outfile, gettrie=False):
    trie = Trie()

    if gettrie == True:
        trie.load_data(wordsfile)
        trie.build()
        trie.save_in_json("./trie_parameter.json")
    
    trie.load_from_json("./trie_parameter.json")
    fmm_trie_segger = FMM()
    fmm_trie_segger.load_dict(wordsfile)
    show_sent_info(fmm_trie_segger, "FMM+Trie")
    
    starttime = time.clock()
    fmm_trie_segger.test(testfile, outfile, _method=trie.get_largest_word) # 将Trie查询作为默认_method方法
    return time.clock() - starttime

'''
词频表的DP算法:因为没有词频数据文件，因此加载其他数据集文件
问题：默认关闭预测
'''
def Words_Freq_DP_test(wordsfile, testfile1, outfile, open=False):
    dp_words = "./data/sougo/SogouLabDic.dic"
    wfdp_segger = Words_Freq_DP()
    wfdp_segger.load_data(dp_words)
    show_sent_info(wfdp_segger, "DP")
    if open == False:
        return None
    
    starttime = time.clock()
    wfdp_segger.test(test_file, out__file)
    return time.clock() - starttime
    
'''
Trie测试
'''
def Trie_test(gettrie=False):
    ti = Trie()
    ti.load_data(word_file)
    ti.build()
    testcase = [
        "１１２３项", "义演", "佳酿", "沿街", "老理", "三四十岁", "解波", "统建", "蓓蕾", "张国鑫", "江泽民",
    ]
    for case in testcase:
        print(case, ti.find(case))

if __name__ == "__main__":
    
    word_file = "./data/icwb2-data/gold/msr_training_words.txt"   
    test_file = "./data/icwb2-data/testing/msr_test.txt"
    out__file = "./data/icwb2-data/scripts/outfile.txt"

    method_list = [FMM_test, BMM_test, BM_test, Words_Freq_DP_test, Trie_FMM_test]
    name_list = ["FMM_test", "BMM_test", "BM_test", "Words_Freq_DP_test(_OFF_)", "Trie_FMM_test"]
    time_list = [] # 程序执行时间=cpu时间 + io时间 + 休眠或者等待时间
    
    for now_method in method_list:
        time_list.append(now_method(word_file, test_file, out__file))
        
    for i in range(len(name_list)):
        print("[", name_list[i], "] method, time:", time_list[i])
