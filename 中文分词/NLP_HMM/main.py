#!/usr/bin/env python
# coding=utf-8

from package.HMM import HMModel
from package.HMMSegger import HMMSegger
import time 

'''
HMM_test代码还不优美
'''
def HMM_test(trainfile, testfile, outfile, dotrain=False):
    segger = HMMSegger()
    segger.load_data(trainfile)
    if dotrain == True:
        segger.train()
        segger.save_in_json("./hmm_parameter.json")
    # segger.output()
    # segger._test()
    segger.load_from_json("./hmm_parameter.json")    

    starttime = time.clock()
    segger.test(testfile, outfile)
    return time.clock() - starttime
    

if __name__ == "__main__":
    trainfile = "./data/icwb2-data/training/msr_training.txt"
    test_file = "./data/icwb2-data/testing/msr_test.txt"
    out__file = "./data/icwb2-data/scripts/outfile.txt"
    spend_time = HMM_test(trainfile, test_file, out__file)
    print("[ HMM _test] method, time: ", spend_time)
