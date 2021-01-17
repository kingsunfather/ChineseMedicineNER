#!usr/bin/env python
# -*- coding:utf-8 -*-
"""
    @Time: 2020-09-28
    @Author: menghuanlater
    @Software: Pycharm 2019.2
    @Usage:
-----------------------------
    Description:
-----------------------------
"""
import pickle
import os
from random import seed, shuffle
import re

output = {
    "query_map": {
        "dru": "找出所有的药物:指用于预防、治疗、诊断疾病并具有康复与保健作用的物质，"
               "主要来源是天然药及其加工品，包括植物药、动物药、矿物药及部分化学、生物制品类药物，如六味地黄丸等",
        "dis": "找出所有的疾病:指人体在一定原因的损害性作用下，因自稳调节紊乱而发生的异常生命活动过程，是特定的异常病理情形，"
               "而且会影响生物体的部分或是所有器官，伴随着特定的症状及医学征象，如高血压、心绞痛、糖尿病等",
        "sym": "找出所有的症状:指疾病过程中机体内的一系列机能、代谢和形态结构异常变化所引起的病人主观上的异常感觉或某些客观病态改变，"
               "如头晕、心悸、小腹胀痛等",
        "pro": "找出所有的医疗程序:指为帮助患有医疗状况的患者而执行的一系列操作，也可以用来诊断疾病或治疗疾病"
               "如免疫学方法、抗体检测等",
        "equ": "找出所有的医疗设备:是指单独或者组合使用于人体的仪器、设备、器具、材料或者其他物品，也包括所需要的软件，"
               "如显微镜、心导管等",
        "ite": "找出所有的医学检验项目:包括渗透压、肾溶质负荷和组成成分等",
        "bod": "找出所有的身体:指人的身体物质和身体部位，如脾脏、肝脏等",
        "dep": "找出所有的科室:指医院的医疗科室，包括眼科、儿科和口腔科等",
        "mic": "找出所有的微生物类:如寄生虫成虫等"
    },
    "train_items": [],
    "valid_items": [],
    #"test_items": [],
    "max_dec_len_map": dict(),
    "answer_category_distribution": dict()
}


def construct_query_context(q_type, context):
    query = output["query_map"][q_type]
    r = []
    if len(context) <= 509 - len(query):
        r.append({"query": query, "context": context, "distance": 0, "start": 0, "type": q_type})
    else:
        d, s = 0, 0
        while True:
            if len(context[d:]) <= 509 - len(query):
                r.append({"query": query, "context": context[d:], "distance": d, "start": s, "type": q_type})
                break
            else:
                x = 0
                while context[d + 509 - len(query) - 1 - x] not in [" ", "\t", "，", "。"]:
                    x += 1
                r.append({"query": query, "context": context[d:(d + 509 - len(query) - x)], "distance": d, "start": s, "type": q_type})
                s = 509 - len(query) - x - 200
                d += 200
    return r


def get_test_items(path):
    test_items = []
    test_txt = [i for i in os.listdir(path)]
    for txt in test_txt:
        digit = int(txt[:-4])
        context = open(os.path.join(path, "%s" % txt), "r", encoding="UTF-8").readline()
        t = {"id": str(digit), "query": []}
        test_items.append(t)
        for key in output["query_map"].keys():
            q_c_pairs = construct_query_context(key, context)
            t["query"].extend(q_c_pairs)
    return test_items


if __name__ == '__main__':
    train_path = "../data/pretrain/data.txt"
    with open(train_path, 'r') as rfile:
        data = rfile.readlines()
    seed(0)
    shuffle(data)
    train_txt, valid_txt = train_txt[200:], train_txt[:200]
    for txt in train_txt:
        fields = txt.split("|||")[:-1]
        context, ann = fields[0], fields[1:]
        src = []
        for item in ann:
            t = re.split("    ", item)
            s, e, q_type = t[0], t[1], t[2]
            label = context[int(s):int(e)+1]
            src.append({"type": q_type, "start": int(s), "end": int(e), "label": label})
            if q_type not in output["answer_category_distribution"].keys():
                output["answer_category_distribution"][q_type] = 1
            else:
                output["answer_category_distribution"][q_type] += 1
            if q_type not in output["max_dec_len_map"].keys():
                output["max_dec_len_map"][q_type] = len(label)
            else:
                if len(label) > output["max_dec_len_map"][q_type]:
                    output["max_dec_len_map"][q_type] = len(label)
        for key in output["query_map"].keys():
            q_c_pairs = construct_query_context(key, context)
            for item in q_c_pairs:
                item["answer"] = []
                i_s, i_e = item["distance"] + item["start"], item["distance"] + len(item["context"]) - 1
                for jtem in src:
                    if jtem["type"] == key and jtem["start"] >= i_s and jtem["end"] <= i_e:
                        item["answer"].append({"ans_s": jtem["start"], "ans_e": jtem["end"], "ans_label": jtem["label"]})
            output["train_items"].extend(q_c_pairs)
    
    for i in range(3):
        shuffle(output["train_items"])
    
    for txt in valid_txt:
        fields = txt.split("|||")[:-1]
        context, ann = fields[0], fields[1:]
        t = {"query": [], "answer": []}
        output["valid_items"].append(t)
        for item in ann:
            t = re.split("    ", item)
            s, e, q_type = t[0], t[1], t[2]
            label = context[s:e+1]
            t["answer"].append({"type": q_type, "ans_s": int(s), "ans_e": int(e), "label": label})
        for key in output["query_map"].keys():
            q_c_pairs = construct_query_context(key, context)
            t["query"].extend(q_c_pairs)
   
    print(len(output["train_items"]))
    # print(output["max_dec_len_map"])
    print(output["answer_category_distribution"])
    with open("../user_data/tmp_data/pretrain_process.pkl", "wb") as f:
       pickle.dump(output, f)
