#!/usr/bin/env python3

import json

with open("extracted.json") as f:
    sent = json.load(f)

fileNum = 13056

file = [x for x in sent if x["docnum"] == fileNum]
file = sorted(file, key=lambda x: (x["parId"], x["parPos"]))

paragraphs = list(set([x["parId"] for x in file]))
print(paragraphs)

for p in paragraphs:
    toPrint = " ".join([x["text"] for x in file if x["parId"] == p])
    print(toPrint)
    print("*****************")
