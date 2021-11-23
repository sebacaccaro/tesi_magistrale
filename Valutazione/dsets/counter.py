import json


def countChars(dset: list):
    return sum([len(d["text"]) for d in dset])


def openAndCount(filename: str):
    with open(filename) as f:
        dset = json.load(f)
    print(f"{filename} -- {countChars(dset)}")


for fn in ["dataset_v2f_reduced.json", "dataset_v2f_reduced_50.json"]:
    openAndCount(fn)