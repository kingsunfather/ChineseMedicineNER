import glob
import json
import os

path = "final_clean"
kw2cls = dict()
kws = []
dumplicate = set()
for rfile in glob.glob("final_clean/*.json"):
    tmp_dict = json.load(open(rfile, encoding="UTF-8"))
    dumplicate = dumplicate | (kw2cls.keys() & tmp_dict.keys())
    kw2cls.update(tmp_dict)

print(f"{len(kw2cls)}")
for kw in dumplicate:
    del kw2cls[kw]

with open("ext_vocab.json", "w", encoding="UTF-8") as wfile:
    json.dump(kw2cls, wfile, ensure_ascii=False)

