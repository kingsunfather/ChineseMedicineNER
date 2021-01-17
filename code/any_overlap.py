# -*- coding: utf-8 -*-
import os
import re

train_path = "../data/train"
#train_path = "../submit"
ids = [int(i[:-4]) for i in os.listdir(train_path) if '.ann' in i]

for tid in ids:
    #text = open(os.path.join(train_path, f'{tid}.txt'), 'r', encoding='utf-8').read()
    anns = open(os.path.join(train_path, f'{tid}.ann'), 'r', encoding='utf-8').readlines()

    items = []
    for item in anns:
        t = re.split("\s", item)
        q_type, s, e, label = t[1], t[2], t[3], t[4]
        items.append((s, e, label, q_type))
        if len(label) == 1:
            print(s, e, label, q_type)

    #items = sorted(items)
    #for i in range(len(items[1:])):
    #    if items[i-1][1] >= items[i][0]:
    #        pass
    #        #print(items[i-1], items[i])
    #        #print(text)
