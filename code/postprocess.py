# -*- coding:utf-8 -*-
import os
import re
import json


#text_path = "/tcdata/juesai"
text_path = "../data/train"
ann_path = "../result"
out_path = "../result_final"
ext_vocab_file = "ext_vocab.json"
if not os.path.exists(out_path):
    os.makedirs(out_path)

text_ids = [int(ann[:-4]) for ann in os.listdir(ann_path) if ".ann" in ann]
# 加载外部词表
with open(ext_vocab_file, encoding="UTF-8") as rfile:
    kw2cls = json.load(rfile)
    if "" in kw2cls:
        del kw2cls[""]

# 遍历文件
for i, tid in enumerate(text_ids):
    text = open(os.path.join(text_path, "%d.txt" % tid), encoding="UTF-8").read()
    anns = open(os.path.join(ann_path, "%d.ann" % tid), encoding="UTF-8").readlines()
    entities = [] 
    labels = []
    # 获取模型的标注
    for item in anns:
        t = re.split("\s", item)
        q_type, s, e, label = t[1], t[2], t[3], t[4]
        labels.append(label)
        entities.append({"cls": q_type, "s": int(s), "e": int(e), "label": label, "from": "model"})

    # 字典匹配新的标注（阅读越长的词越靠前）
    out_kws = sorted(set(kw2cls.keys()) - set(labels), key=len, reverse=True)
    for kw in out_kws:
        p = 0
        if kw == "":
            continue
        while True:
            p = text.find(kw, p)
            if p == -1:
                break
            any_overlap = False
            for e in entities:
                # 判断是否有重合交叉等情况
                if not (e["s"] >= p+len(kw) or e["e"] <= p):
                    any_overlap = True
                    #print(f"{tid}.ann: {e}, {kw}")

            # 没有重合或交叉则添加该实体
            if not any_overlap:
                entities.append({"cls": kw2cls[kw], "s": p, "e": p+len(kw), "label": kw, "from": "vocab"})
                assert text[p:p+len(kw)] == kw
                print(f"{tid}.ann find new entity {kw} at ({p},{p+len(kw)}).")
            p += len(kw)

    # 写文件
    with open(os.path.join(out_path, "%d.ann" % tid), "w", encoding="UTF-8") as wfile:
        for i, e in enumerate(entities):
            wfile.write(f"T{i+1}\t{e['cls']} {e['s']} {e['e']}\t{e['label']}\n")

        if len(entities) == 0:
            wfile.write("")

    #if i == 10:
    #    break
