from gensim import models
from gensim.models import Word2Vec
from nltk import word_tokenize
from tqdm import tqdm
import json
import os


def perturbed_iterator(dataset, setting):
    for sample in dataset:
        tokens = word_tokenize(sample["perturbed"][setting])
        tokens = [t.lower() for t in tokens]
        yield tokens


def make_model(dataset, setting):
    pert_sent = list(perturbed_iterator(dataset, setting))
    model = Word2Vec(pert_sent)
    model.save(f'word2vec_models/{setting}.bin')


with open("../../Creazione_Dataset/dataset.json") as f:
    print("Caricando dataset in memoria....")
    dataset = json.load(f)
    pertubation_settings = list(dataset[0]["perturbed"].keys())

doneModels = (list(os.listdir("./word2vec_models")))
doneModels = [m[:-4] for m in doneModels if "placeholder" not in m]
pertubation_settings = [m for m in pertubation_settings if m not in doneModels]
doneModels = ", ".join(doneModels)
print(f"Saltando modelli {doneModels} perchè già presenti")

for setting in tqdm(pertubation_settings, desc="Modellando"):
    make_model(dataset, setting)
