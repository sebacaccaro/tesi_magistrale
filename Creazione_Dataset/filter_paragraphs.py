import json
from tqdm import tqdm


def isFirstParagraph(fragment):
    return fragment["parId"] == 0


def isLastParagraph(fragment, maxes):
    return fragment["parId"] == maxes[fragment["docnum"]]


with open("dataset_v2.json") as f:
    dataset = json.load(f)

docs = set([x["docnum"] for x in tqdm(dataset)])
maxes = {}

for fragment in dataset:
    if fragment["docnum"] not in maxes:
        maxes[fragment["docnum"]] = []
    maxes[fragment["docnum"]].append(fragment["parId"])

maxes = {docnum: max(maxList) for docnum, maxList in maxes.items()}

dataset = [f for f in tqdm(dataset) if not (
    isFirstParagraph(f) or isLastParagraph(f, maxes))]

with open("dataset_v2f.json", "w") as f:
    json.dump(dataset, f, indent=2)
