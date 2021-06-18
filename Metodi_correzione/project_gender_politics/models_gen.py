from gensim import models
from gensim.models import Word2Vec, FastText
from nltk import word_tokenize
from tqdm import tqdm
from gensim.utils import effective_n_jobs
import json
import os


def perturbed_iterator(dataset, setting):
    for sample in dataset:
        tokens = word_tokenize(sample["perturbed"][setting])
        tokens = [t.lower() for t in tokens]
        yield tokens


def make_model_word2vec(dataset, setting):
    pert_sent = list(perturbed_iterator(dataset, setting))
    model = Word2Vec(pert_sent, workers=effective_n_jobs(-1))
    model.save(f'word2vec_models/{setting}.bin')


def make_model_fasttext(dataset, setting):
    pert_sent = list(perturbed_iterator(dataset, setting))
    model = FastText(pert_sent, workers=effective_n_jobs(-1))
    model.save(f'fasttext_models/{setting}.bin')


with open("../../Creazione_Dataset/dataset.json") as f:
    print("Caricando dataset in memoria....")
    dataset = json.load(f)
    pertubation_settings = list(dataset[0]["perturbed"].keys())

print("Creazione modelli word2vec")
doneModels = (list(os.listdir("./word2vec_models")))
doneModels = [m[:-4] for m in doneModels if "placeholder" not in m]
pertubation_settings_w2v = [
    m for m in pertubation_settings if m not in doneModels]
doneModels = ", ".join(doneModels)
if len(doneModels) > 0:
    print(f"Saltando modelli {doneModels} perchè già presenti")

for setting in tqdm(pertubation_settings_w2v, desc="Modellando word2vec"):
    #make_model_word2vec(dataset, setting)
    pass

print("Creazione modelli FastText")
doneModels = (list(os.listdir("./fasttext_models")))
doneModels = [m[:-4] for m in doneModels if "placeholder" not in m]
pertubation_settings_fst = [
    m for m in pertubation_settings if m not in doneModels]
doneModels = ", ".join(doneModels)
if len(doneModels) > 0:
    print(f"Saltando modelli {doneModels} perchè già presenti")


for setting in tqdm(pertubation_settings, desc="Modellando FastText"):
    make_model_fasttext(dataset, setting)
