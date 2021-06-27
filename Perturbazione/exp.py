from pipelines_def import token_pipeline, segmentation_pipeline, fullPipeline
from pipeline import Pipeline, SuperPipeline, TokenizerModule, DetokenizerModule
import json
from perturbation_superpipelines import M2

with open("../../Stronzate e Prove/prob_full.json") as f:
    probs = json.load(f)

probs = probs

probs = [{**x, "pert": M2.run(x["text"])} for x in probs]

with open("outtest.json", "w") as f:
    json.dump(probs, f, indent=2)
