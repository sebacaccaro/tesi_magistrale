import json


def normalize(v: dict):
    return {
        **v, "lev_reduction_per_sentence":
        v["lev_reduction"] / v["total_chars"],
        "total_distance_per_char": v["total_distance"] / v["total_chars"]
    }


def codeConvert(x):
    return {
        **x,
        "corrected_per_perturbation":
        x["corrected_errors"] / x["perturbation_errors"],
        "introduced_per_sample":
        x["introduced_errors"] / x["total_chars"],
        "introduced_per_corrected":
        x["introduced_errors"] / x["corrected_errors"],
    }


def mapdict(v: dict):
    return {k: codeConvert(normalize(v)) for k, v in v.items()}


with open("valutazione_tot.json") as f:
    val = json.load(f)

val = {k: mapdict(v) for k, v in val.items()}

with open("valutazione_2.json", "w") as f:
    json.dump(val, f, indent=2)
