import json
import sys
from tqdm import tqdm
#yapf: disable
sys.path.insert(0, "./..")
from bert_filler import Filler
#yapf enable

def withBertResults(sample:dict,filler:Filler) -> dict:
    results = filler.get_results_unsorted(sample["sentence"])
    results = [{
        "guess": r["token_str"].strip(),
        "score": r["score"],
        "position": index
    } for index,r in enumerate(results)]
    sample["results"] = results
    sample["correct_word"] = sample["correct_word"].strip()
    return sample

def withStats(sample:dict) -> dict:
    # Calcoland posizione della correzione
    # Se non si riesce a correggere rimane -1
    correction = None
    for option in sample["results"]:
        if option["guess"] == sample["correct_word"]:
            correction = option

    sample["correction"] = correction
    del(sample["results"])
    return sample

print("Aprendo il dataset...",end="")
with open("./errorstudy_dataset.json") as f:
    dataset = json.load(f)
print ("Fatto")

print("Inizializzando il correttore...",end="")
filler = Filler(top_k=30)
print("Fatto")

dataset = [withBertResults(d,filler) for d in tqdm(dataset,desc="Calcolando sostituti bert")]
dataset = [withStats(d) for d in tqdm(dataset,desc="Elaborando le statistiche")]

with open("error_study_raw_stats.json",'w')as f:
    json.dump(dataset,f,indent=2)