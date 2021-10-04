import json
from pprint import pprint
from tqdm import tqdm
from Levenshtein import distance
from statistics import median, stdev
import matplotlib.pyplot as plt
import numpy as np
'''
  {
    "sentence": "\u00ab Io so distinguere nel mio cuore quando [MASK] Signore mi dice \u201c svegliati \u201d? Quando mi dice \u201c apri \u201d?",
    "masked_word": "cl",
    "correct_word": "il",
    "pert_level": "text",
    "correction": {
      "guess": "il",
      "score": 0.992168128490448,
      "position": 0
    }
  },
  {
    "sentence": "Nessuna [MASK], nessuna stanchezza \u00e8 mai valsa a sottrarCi alle vostre brame, a farCi",
    "masked_word": "sollecitudinlo",
    "correct_word": "sollecitudine",
    "pert_level": "text",
    "correction": null
  },
'''


def isCorrectionCloseEnough(original, correction, score):
    editDistance = distance(original, correction)
    if len(original) > 10:
        if editDistance < 5:
            return True
    elif len(original) > 5:
        if editDistance < 4:
            return True
    else:
        if editDistance < 3:
            return True
    return False


def getLevOrderPosition(results: list, masked: str, correct: str):
    results = sorted(results, key=lambda x: distance(x["guess"], masked))
    results = [{**x, "lev_position": index} for index, x in enumerate(results)]
    correct_pos = -1
    i = 0
    while i < 30 and correct_pos == -1:
        if results[i]["guess"] == correct:
            correct_pos = results[i]["lev_position"]
        i += 1
    return correct_pos


def closestCorrection(results: list, masked: str):
    return sorted(results, key=lambda x: distance(x["guess"], masked))[0]


def getStats(datapoints: list):
    position_distribution = {index: 0 for index in range(30)}
    levenstein_distribution = {index: 0 for index in range(30)}
    distance_distribution = {index: 0 for index in range(20)}
    datapoints_with_correction = [
        d for d in datapoints if d["correction"] != None and d["correction"]
        ["position"] < 20  # and solo per statistiche sul sistema a 20
    ]
    datapoints_with_no_correction = [
        d for d in datapoints if d["correction"] == None or d["correction"]
        ["position"] > 19  # or solo per statistiche sul sistema a 20
    ]
    found_10 = 0
    found_20 = 0
    found_30 = 0
    total_masked_length = 0
    total_distance = 0
    ratios = []
    discarded = 0
    lev_correct = 0
    not_found = len(datapoints_with_no_correction)
    for d in datapoints_with_correction:
        position = d["correction"]["position"]
        levenstein_distribution[getLevOrderPosition(
            d["results"], d["masked_word"],
            d["correct_word"])] += 1 if position < 20 else 0
        distance_distribution[distance(d["correction"]["guess"],
                                       d["masked_word"])] += 1
        position_distribution[position] += 1
        found_10 += 1 if position < 10 else 0
        found_20 += 1 if position < 20 else 0
        found_30 += 1
        total_masked_length += len(d["masked_word"])
        total_distance += distance(d["masked_word"], d["correct_word"])
        ratios.append(
            len(d["masked_word"]) /
            distance(d["masked_word"], d["correct_word"]))
        lev_correction = closestCorrection(d["results"], d["masked_word"])
        if isCorrectionCloseEnough(d["masked_word"], lev_correction["guess"],
                                   lev_correction["score"]):
            lev_correct += 1 if d["correct_word"] == lev_correction[
                "guess"] else 0
        else:
            discarded += 1

    false_positives = 0
    for d in datapoints_with_no_correction:
        lev_correction = closestCorrection(d["results"], d["masked_word"])
        false_positives += 1 if isCorrectionCloseEnough(
            d["masked_word"], lev_correction["guess"],
            lev_correction["score"]) else 0

    median_distance_ratio = median(ratios)
    std_dev_distance_ratio = stdev(ratios)

    total_samples = len(datapoints)

    correct_choice_perc = (levenstein_distribution[0] / found_20 * 100) - (
        discarded / len(datapoints_with_correction) * 100)

    return {
        "found_10":
        found_10,
        "found_10_perc":
        found_10 / total_samples * 100,
        "found_20":
        found_20,
        "found_20_perc":
        found_20 / total_samples * 100,
        "found_30":
        found_30,
        "found_30_perc":
        found_30 / total_samples * 100,
        "corrections_pos_distribution":
        position_distribution,
        "distance_distribution":
        distance_distribution,
        "avg_distance_ratio":
        total_masked_length / total_distance,
        "median_distance_ratio":
        median_distance_ratio,
        "std_dev_distance_ratio":
        std_dev_distance_ratio,
        "lev_distribution":
        levenstein_distribution,
        "false_negatives_perc":
        discarded / len(datapoints_with_correction) * 100,
        "false_positives_perc":
        false_positives / len(datapoints_with_no_correction) * 100,
        "lev_correct_perc":
        lev_correct / len(datapoints_with_correction) * 100,
        "correct_choice_perc":
        correct_choice_perc,
        "no_correction":
        not_found
    }


def plot_distribution(distribution_dict: dict,
                      pert_level: str,
                      suffix: str,
                      xName: str,
                      yName: str,
                      color: str = "C0"):
    width = 1
    plt.figure(figsize=(16 / 2, 8 / 2))
    plt.subplots_adjust(top=0.963,
                        bottom=0.146,
                        left=0.099,
                        right=0.981,
                        hspace=0.2,
                        wspace=0.2)
    pos = np.arange(len(distribution_dict.keys()))
    ax = plt.axes()
    ax.set_xticks(pos)
    ax.set_xlabel(xName)
    ax.set_ylabel(yName)
    plt.bar(distribution_dict.keys(),
            distribution_dict.values(),
            1,
            color=color)
    plt.savefig(f"distributions/{suffix}_{pert_level}.png")


def plot_overview_results(distribution_dict: dict):
    width = 0.5
    labels = distribution_dict.keys()
    top_10 = [stats["found_10_perc"] for stats in distribution_dict.values()]
    top_20 = [stats["found_20_perc"] for stats in distribution_dict.values()]
    top_30 = [stats["found_30_perc"] for stats in distribution_dict.values()]
    plt.cla()
    plt.figure(figsize=(16 / 2, 8 / 2))
    fig, ax = plt.subplots()
    plt.subplots_adjust(top=0.969,
                        bottom=0.121,
                        left=0.097,
                        right=0.977,
                        hspace=0.2,
                        wspace=0.2)

    ax.bar(labels, top_30, width, label='Found@30')
    ax.bar(labels, top_20, width, label='Found@20')
    ax.bar(labels, top_10, width, label='Found@10')

    ax.set_ylabel('Correzioni presenti nei primi n risultati (%)')
    ax.set_xlabel('Catena di perturbazione')
    ax.legend()

    plt.savefig(f"distributions/overview.png")


def plot_correct_percentage(correct_dict: dict,
                            name: str,
                            key_to_explode=None):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    plt.subplots_adjust(top=0.969,
                        bottom=0.031,
                        left=0.055,
                        right=0.953,
                        hspace=0.2,
                        wspace=0.2)
    labels = correct_dict.keys()
    sizes = correct_dict.values()

    fig1, ax1 = plt.subplots()

    explosion = [
        0 if key in key_to_explode else 0.1 for key in correct_dict.keys()
    ] if key_to_explode else None

    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', explode=explosion)
    ax1.axis(
        'equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig(f"distributions/{name}.png")


def getTableFromAttrList(results: dict, attrList: list):
    rows = []
    for key, stats in results.items():
        row = [key]
        for attr in attrList:
            row.append(str(round(stats[attr], 2)))
        rows.append(row)
    # Printing
    for row in rows:
        print("& ".join(row) + "\\\\")


def addPosNegChoises(statDict: dict):
    corret_choice_dict = {
        "Scelte Corrette":
        statDict["correct_choice_perc"],
        "Falsi Negativi":
        statDict["false_negatives_perc"],
        "Scelte Errate":
        100 - statDict["correct_choice_perc"] -
        statDict["false_negatives_perc"]
    }
    non_correct_dict = {
        "Falsi positivi": statDict["false_positives_perc"],
        "Correzioni errate scartate": 100 - statDict["false_positives_perc"]
    }
    corret_choice_dict = {
        key: value * statDict["found_20"]
        for key, value in corret_choice_dict.items()
    }
    non_correct_dict = {
        key: value * statDict["no_correction"]
        for key, value in non_correct_dict.items()
    }
    complete = {**non_correct_dict, **corret_choice_dict}
    correct_keys = ["Scelte Corrette", "Correzioni errate scartate"]
    non_cor_keys = ["Falsi Negativi", "Scelte Errate", "Falsi positivi"]
    correct_choice_ration = sum(
        [value for key, value in complete.items() if key in correct_keys])
    non_corr_choice_ration = sum(
        [value for key, value in complete.items() if key in non_cor_keys])
    total = correct_choice_ration + non_corr_choice_ration
    return {
        **statDict, "correct_choice_perc": correct_choice_ration / total * 100,
        "non_corr_choice_perc": non_corr_choice_ration / total * 100
    }


with open("./error_study_raw_stats.json") as f:
    dataset = json.load(f)

sorted_dataset = {
    "text": [],
    "T1": [],
    "T2": [],
    "T3": [],
    "S1": [],
    "S2": [],
    "S3": [],
    "M1": [],
    "M2": [],
    "M3": [],
    "Combinato": []
}

for d in dataset:
    sorted_dataset[d["pert_level"]].append(d)
    sorted_dataset["Combinato"].append(d)

results = {
    key: getStats(statList)
    for key, statList in tqdm(sorted_dataset.items())
}

for key, value in results.items():
    plot_dict = results[key]["corrections_pos_distribution"]
    plot_distribution(plot_dict, key, "score_order",
                      'Posizionamento nei risultati', 'Frequenza')
    plot_dict = results[key]["lev_distribution"]
    plot_distribution(
        plot_dict,
        key,
        "lev_pos",
        'Posizionamento nei risultati ordinati per la Distanza di Levenshtein',
        'Frequenza',
        color="C1")

results = {key: addPosNegChoises(value) for key, value in results.items()}
comb = results["Combinato"]
pprint(comb)

plot_overview_results(results)
corret_choice_dict = {
    "Scelte Corrette":
    comb["correct_choice_perc"],
    "Falsi Negativi":
    comb["false_negatives_perc"],
    "Scelte Errate":
    100 - comb["correct_choice_perc"] - comb["false_negatives_perc"]
}
plot_correct_percentage(corret_choice_dict, "correct_combinato")
non_correct_dict = {
    "Falsi positivi": comb["false_positives_perc"],
    "Correzioni errate scartate": 100 - comb["false_positives_perc"]
}
plot_correct_percentage(non_correct_dict, "non_correct_combinato")

corret_choice_dict = {
    key: value * comb["found_20"]
    for key, value in corret_choice_dict.items()
}
non_correct_dict = {
    key: value * comb["no_correction"]
    for key, value in non_correct_dict.items()
}
plot_complete = {**corret_choice_dict, **non_correct_dict}

plot_correct_percentage(
    plot_complete,
    "overview_scelte_combinato",
    key_to_explode=["Correzioni errate scartate", "Scelte Corrette"])
getTableFromAttrList(results,
                     ["found_10_perc", "found_20_perc", "found_30_perc"])
getTableFromAttrList(
    results,
    ["correct_choice_perc", "false_negatives_perc", "false_positives_perc"])
getTableFromAttrList(results, ["correct_choice_perc", "non_corr_choice_perc"])
