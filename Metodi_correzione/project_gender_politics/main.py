from ocr import PostOCRTextCorrection
import os
from gensim.models import Word2Vec, FastText
import json

outfolder = "corrections/"


def entryToSetting(entry, setting):
    return {
        **entry,
        "perturbed": entry["perturbed"][setting],
        "corrected": entry["perturbed"][setting],
    }


def writeOutput(output, setting, suffix=""):
    with open(f"{outfolder}{suffix}{setting}.json", "w") as f:
        json.dump(output, f, indent=2)


with open('lexicon.txt') as f:
    lexicon = set(f.read().splitlines())

fst_models = [m[:-4]
              for m in os.listdir("./fasttext_models") if m[-4:] == ".bin"]
w2v_models = [m[:-4]
              for m in os.listdir("./word2vec_models") if m[-4:] == ".bin"]

common_models = [x for x in set(
    [*fst_models, *w2v_models]) if x in fst_models and x in w2v_models]

with open("../../Creazione_Dataset/dataset.json") as f:
    print("Caricando dataset in memoria...")
    dataset = json.load(f)
    print("Fatto!")

i = 0
for model in common_models:
    i += 1
    print(f"--- Correggendo modello {model} ({i}/{len(common_models)}) ---")

    print("Caricando i modelli...")
    w2v_model = Word2Vec.load(f"./word2vec_models/{model}.bin")
    fss_model = FastText.load(f"./fasttext_models/{model}.bin")
    corrector = PostOCRTextCorrection(w2v_model, fss_model, lexicon)

    print("Correzione iniziata...")
    model_dataset = [entryToSetting(entry, model) for entry in dataset]
    corrected_output, error_output = corrector.ocr_correction_corpus(
        model_dataset, key="corrected")

    writeOutput(corrected_output, model)
    writeOutput(error_output, model, "errors_")
