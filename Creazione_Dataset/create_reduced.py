import json
import random

print("Leggendo dataset")
with open("dataset.json") as f:
    dataset = json.load(f)

print("Mescolando dataset")
random.shuffle(dataset)

dataset = dataset[:10000]

print("Scrivendo versione ridotta")
with open("dataset_reduced.json", "w") as f:
    json.dump(dataset, f, indent=2)
