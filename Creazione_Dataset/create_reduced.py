import json
import random

with open("dataset_v2f.json") as f:
    dataset = json.load(f)

random.shuffle(dataset)

dataset = dataset[:10000]

with open("dataset_v2f_reduced.json", "w") as f:
    json.dump(dataset, f, indent=2)
