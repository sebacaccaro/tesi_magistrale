import json
import os
from gensim.models import Word2Vec, FastText
from tqdm import tqdm

min_count = 5
window = 5
vector_size = 100
sample = 1e-4
negative = 20
epochs = 50
min_alpha = 0.0001
alpha = 0.025


def get_models_list():
    fst_models = [m[:-4]
                  for m in os.listdir("../project_gender_politics/fasttext_models") if m[-4:] == ".bin"]
    w2v_models = [m[:-4]
                  for m in os.listdir("../project_gender_politics/word2vec_models") if m[-4:] == ".bin"]

    common_models = [x for x in set(
        [*fst_models, *w2v_models]) if x in fst_models and x in w2v_models]
    return common_models


def updateModel(model, sentences):
    model.build_vocab(sentences, update=True)
    model.train(sentences, epochs=epochs,
                total_examples=model.corpus_count,
                total_words=model.corpus_total_words)


with open("../../Creazione_Dataset/dataset.json") as f:
    sentences = json.load(f)
    sentences = [s["text"] for s in sentences]


model_list = get_models_list()
for modelName in tqdm(model_list, "Aggiornando modelli word2vec"):
    model = Word2Vec.load(
        f"../project_gender_politics/word2vec_models/{modelName}.bin")
    updateModel(model, sentences)
    model.save(f'word2vec_models/{modelName}.bin')

for modelName in tqdm(model_list, "Aggiornando modelli fasttext"):
    model = FastText.load(
        f"../project_gender_politics/fasttext_models/{modelName}.bin")
    updateModel(model, sentences)
    model.save(f'fasttext_models/{modelName}.bin')
