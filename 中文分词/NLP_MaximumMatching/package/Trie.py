#!/usr/bin/env python
# coding=utf-8

import json

class Trie():
    def __init__(self):
        self.data = None  
        self.childs = [{}]
        self.tot = 0
        self.cnt = {}

    def load_data(self, filename):
        self.data = open(filename, "r", encoding="gb18030")
        self.tot = 0
        
    def insert(self, src):
        p = 0
        for i in src:
            if self.childs[p].get(i, -1) == -1:
                # 出现新节点时再添加字典
                self.childs.append({})
                self.childs[p][i] = self.tot + 1
                self.tot += 1
            p = self.childs[p][i]
        
        if self.cnt.get(p, -1) == -1:
            self.cnt[p] = 1
        else:
            self.cnt[p] += 1
    
    def find(self, src):
        p = 0
        pre_word = src[0]
        for i in src:
            if self.childs[p].get(i, -1) == -1:
                return [-1, pre_word]
            p = self.childs[p][i]
            pre_word += i
        if self.cnt.get(p, -1) == -1:
            return [-1, pre_word]
        else:
            return [self.cnt[p], pre_word]
    
    def build(self):
        for word in self.data:
            self.insert(word.strip(" ").strip("\n"))

    def get_largest_word(self, word, dict):
        return self.find(word)[1]
    
    '''
    存储/提取Trie树信息
    '''
    def __set_json_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError 
    
    def save_in_json(self, json_file):
        trie_parameter = {
            "childs" : self.childs, 
            "tot" : self.tot, 
            "cnt" : self.cnt,  
        }
        data = json.dumps(trie_parameter, default=self.__set_json_default)
        data = data.encode('utf-8').decode('unicode-escape') # decode('unicode-escape')来得到汉字
        json_fw = open(json_file, "w", encoding="utf-8")
        json_fw.write(data)

    
    def load_from_json(self, json_file):
        json_fr = open(json_file, "r", encoding="utf-8")
        trie_parameter = json.loads(json_fr.read())
        self.childs = trie_parameter['childs']
        self.tot = trie_parameter['tot']
        self.cnt = trie_parameter['cnt']
    

