from gensim import models
from gensim.models import Word2Vec, FastText
from nltk import word_tokenize
from tqdm import tqdm
from gensim.utils import effective_n_jobs
import json
import os

# Models config
min_count = 5
window = 5
vector_size = 100
sample = 1e-4
negative = 20
epochs = 50
min_alpha = 0.0001
alpha = 0.025
workers = effective_n_jobs(-1)


def perturbed_iterator(dataset, setting):
    for sample in dataset:
        tokens = word_tokenize(sample["perturbed"][setting])
        tokens = [t.lower() for t in tokens]
        yield tokens


def make_model_word2vec(dataset, setting):
    pert_sent = list(perturbed_iterator(dataset, setting))
    model = Word2Vec(pert_sent, min_count=min_count,
                     window=window,
                     vector_size=vector_size,
                     sample=sample,
                     alpha=alpha,
                     negative=negative,
                     workers=workers,
                     min_alpha=min_alpha)
    model.save(f'word2vec_models/{setting}.bin')


def make_model_fasttext(dataset, setting):
    pert_sent = list(perturbed_iterator(dataset, setting))
    model = FastText(pert_sent, min_count=min_count,
                     window=window,
                     vector_size=vector_size,
                     sample=sample,
                     alpha=alpha,
                     negative=negative,
                     workers=workers,
                     min_alpha=min_alpha)
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
    make_model_word2vec(dataset, setting)

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
