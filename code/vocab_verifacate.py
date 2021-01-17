# -*- coding: utf-8 -*-
import os
import re

train_path = "../data/train"
#train_path = "../submit"
ids = [int(i[:-4]) for i in os.listdir(train_path) if '.ann' in i]
inner_vocab = dict()

for tid in ids:
    anns = open(os.path.join(train_path, f'{tid}.ann'), 'r', encoding='utf-8').readlines()

    for item in anns:
        t = re.split("\s", item)
        q_type, s, e, label = t[1], t[2], t[3], t[4]
        if label in inner_vocab:
            if inner_vocab[label] != q_type:
                print(f"{label} has multi type: {inner_vocab[label]}, {q_type}")
        else:
            inner_vocab[label] = q_type

#print(inner_vocab)
        

    #items = sorted(items)
    #for i in range(len(items[1:])):
    #    if items[i-1][1] >= items[i][0]:
    #        pass
    #        #print(items[i-1], items[i])
    #        #print(text)
