#!/usr/bin/env python
# coding=utf-8

from package.SP import ShortPath

if __name__ == "__main__":
    train_words_file = "./data/msr_training_words.utf8"
    # sentence = "津巴布韦获得中国政府资助７５亿新卢布，津巴布韦政府用这些钱来修建基础设施。"
    sentence = "他说的确实在理"
    sp_segger = ShortPath()
    sp_segger.load_data(train_words_file)
    ret_stat = sp_segger.cut(sentence)
    print("offset_list:", sp_segger.offset_list)
    print("find 的确：", sp_segger.trie.find("的确"))