#!/usr/bin/env python
# coding=utf-8

from .HMM import HMModel 
from .extra import seg_stop_words

'''
中文分词问题可以转化为序列标注问题，先定义序列状态
'''
STATES = {"B", "M", "E", "S"}

'''
训练/测试数据使用的是GB2312,GB18030兼容GB2312，GB18030汉字覆盖范围更大
'''
ENCODING_TYPE = "gb18030"


def get_tags(word):
    tags = []
    if len(word) == 1:
        tags = ["S"]
    elif len(word) == 2:
        tags = ["B", "E"]
    else:
        m_words_num = len(word) - 2
        tags.append("B")
        tags.extend(["M"] * m_words_num)
        tags.append("E")
    return tags
    
def cut_sent(sentence, tags):
    word_list = []
    start = -1
    started = False

    if len(tags) != len(sentence):
        return None 
    
    if tags[-1] in {"B", "M"}:
        if len(tags) > 1 and tags[-2] in {"S", "E"}:
            tags[-1] = "S"
        else:
            tags[-1] = "E"
    
    for i in range(len(tags)):
        if tags[i] == 'S':
            if started:
                started = False 
                word_list.append(sentence[start:i])
            word_list.append(sentence[i])
        elif tags[i] == 'B':
            if started:
                word_list.append(sentence[start:i])
            start = i
            started = True
        elif tags[i] == 'E':
            started = False 
            word = sentence[start:i+1]
            word_list.append(word)
        elif tags[i] == 'M':
            continue 

    return word_list

class HMMSegger(HMModel):
    
    def __init__(self, *args, **kwargs):
        super(HMMSegger, self).__init__(*args, **kwargs)
        self.states = STATES 
        self.data = None

    def load_data(self, filename):
        self.data = open(filename, "r", encoding=ENCODING_TYPE)

    def train(self):
        if not self.init_flag:
            self.setup()
        
        for line in self.data:
            # 先处理每行数据首尾空格问题
            line = line.strip()
            if not line:
                continue
            
            observes = []
            for i in range(len(line)):
                if line[i] == " ":
                    continue 
                observes.append(line[i])
            
            words = line.split(" ")
            
            states = []
            for word in words:
                if word == "":
                    continue
                states.extend(get_tags(word))
            self.do_train(observes, states)
    
    def cut(self, sentence):
        tags = self.do_predict(sentence)
        return cut_sent(sentence, tags)

    def _test(self):
        cases = [
            "中共中央总书记、国家主席江泽民",
            "（一九九七年十二月三十一日）",
            "天津市首届检察官艺术节音乐会日前举行（图片）",
            "我有１１１个气球",          
            "１９９８年，中国人民将满怀信心地开创新的业绩。尽管我们在经济社会发展中还面临不少困难，但我们有邓小平理论的指引，有改革开放近２０年来取得的伟大成就和积累的丰富经验，还有其他 的各种有利条件，我们一定能够克服这些困难，继续稳步前进。只要我们进一步解放思想，实事求是，抓住机遇，开拓进取，建设有中国特色社会主义的道路就会越走越宽广。",
            "他拥有世界最大的私人集装箱船队，也要做与中国合作的先行。",
        ]
        for case in cases:
            result = self.cut(case)
            print(result)

    def test(self, testfile, outfile):
        cases = open(testfile, "r", encoding=ENCODING_TYPE)
        fw = open(outfile, "w", encoding=ENCODING_TYPE) 
        for case in cases:
            result = self.cut(case)
            writeStr = ""
            for word in result:
                writeStr = writeStr + str(word) + " "
            fw.write(writeStr.strip(" "))
        cases.close()
        fw.close()
    