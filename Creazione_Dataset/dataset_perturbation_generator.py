from tqdm.utils import _supports_unicode
from tqdm import tqdm
import json
import sys
import nltk
sys.path.insert(0, "../Perturbazione/")
from perturbation_superpipelines import sup_pipelines

nltk.download('punkt')

def perturbed_sample(sample, perturbed, sup_name):
    return {
        **sample,
        "perturbed": {
            **sample["perturbed"],
            sup_name: perturbed
        }
    }


print("Caricando le frasi estratte...")
with open("extracted.json")as f:
    dataset = json.load(f)

dataset = [{**d, "perturbed": {}} for d in dataset]


i = 0
for sup_name, sup in sup_pipelines.items():
    desc = f"Perturbando con {sup_name} ({i}/{len(sup_pipelines)})"
    i += 1
    dataset = [perturbed_sample(s, sup.run(s["text"]), sup_name)
               for s in tqdm(dataset, desc=desc)]

with open("dataset_v2.json", "w") as f:
    json.dump(dataset, f, indent=2)
