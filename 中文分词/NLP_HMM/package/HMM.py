#!/usr/bin/env python
# coding=utf-8

import json 

EPS = 0.000001
ext = 1000.0

'''
    HMM => (A, B, Pi, S, O)

    A : trans_mat
        trans_mat 为一个 self.states X self.states 大小的矩阵
        其数值表示状态转移概率

    B : obser_mat
        obser_mat 为一个 self.states行 的二维概率表
        B[j][k] 状态为j观测为k

    Pi : init_vect
        init_vect 表示初始概率向量

    因为把中文分词问题转化为了序列标注问题，所以可能的状态有四种{"Begin", "Middle", "End", "Single"}

'''

class HMModel():

    def __init__(self):
        self.trans_mat = {} 
        self.obser_mat = {} 
        self.init_vect = {} 
        self.init_flag = False
        self.state_count = {} 
        self.states = {}
    
    def setup(self):
        for state in self.states:
            self.trans_mat[state] = {}      
            for taget in self.states:   
                self.trans_mat[state][taget] = 0.0
            self.obser_mat[state] = {}      
            self.init_vect[state] = 0 
            self.state_count[state] = 0 
        self.init_flag = True
    
    '''
    使用监督学习算法，利用极大似然估计来估计HMM参数(A, B, PI)
    通过记录频率来估计参数
    传入观测序列与状态序列均为中文，所以采用dict来做一个映射
    一个观测序列对应一个状态序列
    '''
    def do_train(self, observes, states):
        if not self.init_flag:
            self.setup()
        
        for i in range(len(states)):
            if i == 0:
                self.init_vect[states[i]] += 1      # 统计初始概率向量频数
                self.state_count[states[i]] += 1    # 统计状态频数
            else:
                self.trans_mat[states[i - 1]][states[i]] += 1   # 统计前一个状态转移到后一个状态的频数
                self.state_count[states[i]] += 1 
            
            if observes[i] not in self.obser_mat[states[i]]:
                self.obser_mat[states[i]][observes[i]] = 1
            else:
                self.obser_mat[states[i]][observes[i]] += 1

    '''
    Q : 对三个概率分布放大不同的倍数得到的准确率也不同
    A : 在本目录下的 HMM_parameter_record 文件中已经做出了测试
    '''
    def get_frequency(self):
        trans_mat = {}
        obser_mat = {}
        init_vect = {}
        default = max(self.state_count.values())

        # 计算状态转移概率
        for key1 in self.trans_mat:
            trans_mat[key1] = {}
            for key2 in self.trans_mat[key1]:
                if self.state_count[key1] != 0:
                    trans_mat[key1][key2] = float(self.trans_mat[key1][key2] * ext) / self.state_count[key1]
                else:
                    trans_mat[key1][key2] = float(self.trans_mat[key1][key2] * ext) / default   

        # 计算观测概率
        for key1 in self.obser_mat:
            obser_mat[key1] = {}
            for key2 in self.obser_mat[key1]:
                if self.state_count[key1] != 0:
                    obser_mat[key1][key2] = float(self.obser_mat[key1][key2] + 1) / self.state_count[key1]
                else:
                    obser_mat[key1][key2] = float(self.obser_mat[key1][key2] + 1) / default

        # 计算初始状态概率
        for key in self.init_vect:
            if self.state_count[key] != 0:
                init_vect[key] = float(self.init_vect[key] * ext) / self.state_count[key]
            else:
                init_vect[key] = float(self.init_vect[key] * ext) / default
        
        return trans_mat, obser_mat, init_vect
    
    '''
    预测算法采用viterbi算法
    Xi[t]  = dict{i, val}代表在时刻t状态为i的所有单个路径(i1,i2,...it)中概率最大值
    Psi[t] = val 代表在时刻t状态为i的所有单个路径(i1,i2,...it)中概率最大值的路径第t-1个节点
    '''
    def do_predict(self, OSequence):
        Xi  = [{}]  
        Psi = {}    
        trans_mat, obser_mat, init_vect = self.get_frequency()
        # 初始化
        for state in self.states:
            Xi[0][state] = init_vect[state] * obser_mat[state].get(OSequence[0], EPS)
            Psi[state] = [state] 
        
        # 递推过程
        for t in range(1, len(OSequence)):
            Xi.append({})
            new_Psi = {}
            for i in self.states:
                items = []
                for j in self.states:
                    # 没有在train中出现的字会导致dict访问错误，因此使用dict.get(,default)方法
                    prob = Xi[t - 1].get(j, EPS) * trans_mat[j].get(i, EPS) * obser_mat[i].get(OSequence[t], EPS)
                    items.append((prob, j))
                best = max(items) # best : (prob, j)
                Xi[t][i] = best[0]
                new_Psi[i] = Psi[best[1]] + [i] 
            Psi = new_Psi

        # 求得最大概率及其最佳路径起点
        prob, state = max([(Xi[len(OSequence) - 1].get(state, EPS), state) for state in self.states])
        return Psi[state]

    '''
    输出训练之后得到的数据
    '''
    def output(self):
        print("trans_mat:")
        for state in self.trans_mat:
            print(state,":",self.trans_mat[state])
        print("init_vect:")
        for state in self.init_vect:
            print(state,":",state)
        print("obser_mat:")
        for state in self.obser_mat:
            print(state,":",self.obser_mat[state])

    '''
    考虑到模型重复使用问题，因此直接将模型参数保存至本地json文件中
    TypeError: Object of type 'set' is not JSON serializable
    Stackoverflow解决方案:
        https://stackoverflow.com/questions/22281059/set-object-is-not-json-serializable
    '''
    def __set_json_default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError 

    '''
    将模型参数保存在对应的json文件中
    '''
    def save_in_json(self, json_file):
        hmm_parameter = {
            "trans_mat" : self.trans_mat, 
            "obser_mat" : self.obser_mat, 
            "init_vect" : self.init_vect, 
            "state_count" : self.state_count, 
            "states" : self.states, 
        }
        data = json.dumps(hmm_parameter, default=self.__set_json_default)
        data = data.encode('utf-8').decode('unicode-escape') # decode('unicode-escape')来得到汉字
        json_fw = open(json_file, "w", encoding="utf-8")
        json_fw.write(data)

    '''
    将模型参数从对应的json文件中提取出来
    '''
    def load_from_json(self, json_file):
        json_fr = open(json_file, "r", encoding="utf-8")
        hmm_parameter = json.loads(json_fr.read())
        self.trans_mat = hmm_parameter['trans_mat']
        self.obser_mat = hmm_parameter['obser_mat']
        self.init_vect = hmm_parameter['init_vect']
        self.state_count = hmm_parameter['state_count']
        self.states = hmm_parameter['states']
        self.init_flag = True
        