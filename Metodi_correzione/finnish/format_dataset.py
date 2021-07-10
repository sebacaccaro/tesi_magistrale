import json

with open("../../Creazione_Dataset/dataset_reduced.json") as json_file:
    dataset = json.load(json_file)

dataset = [d["text"] for d in dataset]

with open("dataset.txt", "w") as f:
    for line in dataset:
        f.write(line + "\n")
