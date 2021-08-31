#!/usr/bin/env python3
from bert_filler import Filler
from tokencorrector import TokenCorrector
import json
from tqdm import tqdm

filler = Filler()
corrector = TokenCorrector("lexicon.txt", filler)


with open("../../Creazione_Dataset/dataset_v2f_reduced.json") as f:
    dataset = json.load(f)

dataset = [{
    "text": datapoint["text"],
    "perturbed": datapoint["perturbed"]["T3"],
    "corrected": corrector.correct(datapoint["perturbed"]["T3"])
} for datapoint in tqdm(dataset)
]

with open("correction_output.json", "w") as f:
    json.dump(dataset, f, indent=2)
