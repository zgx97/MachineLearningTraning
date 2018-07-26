#!/usr/bin/env python
# coding=utf-8

from .Trie import Trie 
from os.path import exists as file_exists

'''
实现最短路径分词算法
'''
class ShortPath:
    def __init__(self):
        self.trie = Trie() 

    def load_data(self, filename, check_json=True, json_file="./trie_dict.json"):
        # if file_exists(json_file) and check_json:
        #     self.trie.load_from_json(json_file)
        # else:
        #     self.trie.load_data(filename)
        #     self.trie.build()
        #     self.trie.save_in_json(json_file)
        
        self.trie.load_data(filename)
        self.trie.build()
        # self.trie.save_in_json(json_file)
        self.offset_list = None
        self.offset_flag = False 
        self.G = []
    
    # 可以优化
    def offset(self, sentence):
        slen = len(sentence)
        ret_stat = []
        for i in range(slen):
            ret_stat.append([])
            all_prefix = self.trie.find_all_prefix(sentence[i:])
            if len(all_prefix) == 0:
                continue
            for sub_prefix in all_prefix:
                ret_stat[i].append(sub_prefix)

        self.offset_list = ret_stat
        self.offset_flag = True 

    def build_grap(self, sentence):
        G_size = len(sentence)+1
        # self.G = [[0 for j in range(G_size)] for i in range(G_size)]
        self.G = [[] for i in range(G_size)]
        for i in range(G_size-1):
            for j in self.offset_list[i]:
                # self.G[i].append({"v":i+len(j), "w":1})
                self.G[i].append((i+len(j), 1))
                # self.G[i][i+len(j)] = 1
        # for i in range(G_size):
        #     print(i, ":", self.G[i])
    
    # 从0到len(sentence)的最短路
    def Djikstra(self, sentence):
        G_size = len(sentence)+1
        INF = 1024
        vis = [False for i in range(G_size)]
        dis, pre_ind = [INF for i in range(G_size)], [INF for i in range(G_size)]

        dis[0], pre_ind[0] = 0, -1
        # 优化查询效率
        for i in range(G_size):
            u = None 
            min_w = INF
            for j in range(G_size):
                if (vis[j] == False) and (dis[j] < min_w):
                    min_w = dis[j]
                    u = j
            # 没有可用的顶点，算法结束，说明有顶点无法从源点到达
            if min_w == INF:
                return False
            vis[u] = True  # 将顶点 v 加入集合 U 中
            for edge in self.G[u]:
                _v, _w = edge[0], edge[1]
                if (vis[_v] == False) and (dis[u] + _w < dis[_v]) and (_w != 0):
                    dis[_v] = dis[u] + _w
                    pre_ind[_v] = u

        # print("dis arr:", dis)
        # print("pre_ind:", pre_ind)
        cut_stat = []

        nind = G_size-1
        pind = pre_ind[nind]
        
        while pind != -1:
            cut_stat.append(sentence[pind:nind])
            nind = pind
            pind = pre_ind[nind]
    
        cut_stat.reverse()
        # print("cut_stat:", cut_stat)
        # print("dist arr:", dis)
        # print("Shortest Path:", dis[G_size-2])
        return cut_stat

    def cut(self, sentence):
        self.offset(sentence)
        self.build_grap(sentence)
        ret_stat = self.Djikstra(sentence)
        print("ret_stat:", ret_stat)
    
if __name__ == "__main__":
    pass
