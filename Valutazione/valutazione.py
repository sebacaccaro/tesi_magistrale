import os
from tqdm import tqdm
import json
from Levenshtein import matching_blocks, editops, distance

corrections_folders = {
    "bert1": "../Metodi_correzione/bert/corrections/v_100/",
    "pgp01a": "../Metodi_correzione/project_gender_politics/corrections/v_100/"
    # "pgp02a": "../Metodi_correzione/project_gender_politics_advanced/corrections/",
    # "pgp01b": "../Metodi_correzione/project_gender_politics_2/corrections/" """
}


def diffAlign(s1, s2):
    matching = matching_blocks(
        editops(s1, s2), s1, s2)
    s1 = [c for c in s1]
    s2 = [c for c in s2]
    s1n = []
    s2n = []
    popped1, added1 = 0, 0
    popped2, added2 = 0, 0
    for mb in matching:
        index1 = mb[0]
        index2 = mb[1]
        # Controllo allineamento indici
        while(popped1 < index1):
            s1n.append(s1.pop(0))
            popped1 += 1
        while(popped2 < index2):
            s2n.append(s2.pop(0))
            popped2 += 1
        while(len(s1n) < len(s2n)):
            s1n.append("$")
            added1 += 1
        while(len(s2n) < len(s1n)):
            s2n.append("$")
            added2 += 1

        seqLen = mb[2]
        for i in range(seqLen):
            s1n.append(s1.pop(0))
            s2n.append(s2.pop(0))
            popped1, popped2 = popped1 + 1, popped2 + 1

    s1n = "".join(s1n)
    s2n = "".join(s2n)
    return s1n, s2n


def align(datapoint):
    s1, s2 = diffAlign(
        str.strip(datapoint["text"]), str.strip(datapoint["perturbed"]))
    s1f, s2f = s1, s2
    s2, s3 = diffAlign(s2, str.strip(datapoint["corrected"]))
    s1, s3 = diffAlign(s1, s3)
    if len(s1) == len(s2) == len(s3):
        return s1, s2, s3, True
    else:
        return s1f, s2f, s3, False


def errorBitMask(c, cp, cpp):
    return [0 if c[i] == cp[i] == cpp[i] else 1 for i in range(len(c))]


def bitMaskToPos(bitmask):
    ranges = []
    current = []
    for i in range(len(bitmask)):
        value = bitmask[i]
        if value == 0:
            if len(current) > 0:
                ranges.append(current)
                current = []
        elif value == 1:
            current.append(i)
    if len(current) > 0:
        ranges.append(current)
    return ranges


def errorChars(sentence, ranges):
    return ["".join([sentence[i] for i in r]) for r in ranges]


def standardScore(c, cp, cpp):
    errors = bitMaskToPos(errorBitMask(c, cp, cpp))
    c = errorChars(c, errors)
    cp = errorChars(cp, errors)
    cpp = errorChars(cpp, errors)
    perturbation_errors = sum([1 for i in range(len(c)) if c[i] != cp[i]])
    corrected_errors = sum(
        [1 for i in range(len(c)) if c[i] != cp[i] and cpp[i] == c[i]])
    introduced_errors = sum(
        [1 for i in range(len(c)) if c[i] == cp[i] and cpp[i] != c[i]])
    return {
        "perturbation_errors": perturbation_errors,
        "corrected_errors": corrected_errors,
        "introduced_errors": introduced_errors,
    }


def errorScore(c, cp, cpp):
    errors = bitMaskToPos(errorBitMask(c, cp, cp))
    c = errorChars(c, errors)
    cp = errorChars(cp, errors)
    perturbation_errors = sum([1 for i in range(len(c)) if c[i] != cp[i]])
    corrected_errors = 0
    introduced_errors = perturbation_errors
    return {
        "perturbation_errors": perturbation_errors,
        "corrected_errors": corrected_errors,
        "introduced_errors": introduced_errors,
    }


def correctionScore(sample):
    c = sample["original_aligned"]
    cp = sample["perturbed_aligned"]
    cpp = sample["corrected_aligned"]
    return standardScore(c, cp, cpp) if sample["alignedSuccess"] else errorScore(c, cp, cpp)


def calculate_distance(original: str, perturbed: str, corrected: str) -> int:
    """ 
    Returns tLev-distance between original-corrected
    """
    original = str.strip(original)
    perturbed = str.strip(perturbed)
    corrected = str.strip(corrected)
    return distance(original, corrected)


def calculate_distance_reduction(original: str, perturbed: str, corrected: str) -> int:
    """ 
    Returns the net reduction in Lev-distance between orginal-perturbed and perturbed-corrected
    """
    original = str.strip(original)
    perturbed = str.strip(perturbed)
    corrected = str.strip(corrected)
    return distance(original, perturbed) - distance(original, corrected)


def dataset_stats(dataset):
    dataset = [{"stats": align(datapoint), **datapoint}
               for datapoint in tqdm(dataset, desc="    > Allineando Frasi")]
    dataset = [{
        # Allineamento
        "original_aligned": x["stats"][0],
        "perturbed_aligned": x["stats"][1],
        "corrected_aligned": x["stats"][2],
        "alignedSuccess": x["stats"][3],
        # Levenstein Distances
        "distance_red": calculate_distance_reduction(x["text"], x["perturbed"], x["corrected"]),
        "distance": calculate_distance(x["text"], x["perturbed"], x["corrected"])
        ** x
    } for x in dataset]
    # Summing up lev net distance
    total_lev_reduction = sum([x["distance_red"] for x in dataset])
    total_distance = sum([x["distance"] for x in dataset])
    dataset = [correctionScore(sample) for sample in tqdm(
        dataset, desc=" > Valutando Correzioni")]
    stats = {
        "perturbation_errors": sum([x["perturbation_errors"] for x in dataset]),
        "corrected_errors": sum([x["corrected_errors"] for x in dataset]),
        "introduced_errors": sum([x["introduced_errors"] for x in dataset]),
        "lev_reduction": total_lev_reduction,
        "total_distance": total_distance,
        "total_samples": len(dataset)
    }
    return stats


def fileNameToStats(filename, correction_folder):
    print(f"    > Valutando {dataset_name(filename)}...")
    with open(correction_folder + filename) as f:
        corrections = json.load(f)
    return dataset_stats(corrections)


def dataset_name(filename):
    return filename.replace(".json", "")


def evaluate_project(project_foler, corr_name):
    print(f"Valutando {corr_name}...")
    files = os.listdir(project_foler)
    files = [f for f in files if ".json" in f and "errors_" not in f]
    stats = {dataset_name(f): fileNameToStats(f, project_foler) for f in files}
    return stats


stats = {corr_name: evaluate_project(
    corr_folder, corr_name) for corr_name, corr_folder in tqdm(corrections_folders.items())}

with open("valutazione.json", "w")as f:
    json.dump(stats, f, indent=2)

print("Fatto! Output scritto in valutaizone.json")
