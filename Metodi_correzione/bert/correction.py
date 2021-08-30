#!/usr/bin/env python3
from nltk import data
from bert_filler import Filler
from corrector import Corrector
import json
from tqdm import tqdm

filler = Filler()
corrector = Corrector("lexicon.txt", filler)


with open("../../Creazione_Dataset/dataset_v2f_reduced.json") as f:
    dataset = json.load(f)


def evalCorrection(dataset, pertMode):
    dataset = [{
        **datapoint,
        "text": datapoint["text"],
        "perturbed": datapoint["perturbed"][pertMode],
        "corrected": corrector.correct(datapoint["perturbed"][pertMode])
    } for datapoint in tqdm(dataset, desc=f"Correcting {pertMode}")
    ]
    with open(f"corrections/{pertMode}.json", "w") as f:
        json.dump(dataset, f, indent=2)


for pertMode in ["T1", "T2", "T3", "S1", "S2", "S3", "M1", "M2", "M3"]:
    evalCorrection(dataset, pertMode)
