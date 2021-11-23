import json

sup = [
    "M1",
    "M2",
    "M3",
    "S1",
    "S2",
    "S3",
    "T1",
    "T2",
    "T3",
]

dsets = ["Bert@50", "Ftwv@50", "Bert@100", "Ftwv@100"]

with open("valutazione_2.json") as f:
    stats = json.load(f)


def isolate(perstat: dict, statName: str):
    return {k: v[statName] for k, v in perstat.items()}


def mapToStat(stats: dict, statName: str):
    return {k: isolate(v, statName) for k, v in stats.items()}


def printLine(statdict: dict, pertLevel: str):
    linestr = pertLevel
    for dset in dsets:
        linestr += f"& {round(statdict[dset][pertLevel],4)}"
    linestr += "\\\\"
    print(linestr)


def printTable(stats: dict, statName: str):
    statdict = mapToStat(stats, statName)
    for pertLevel in sup:
        printLine(statdict, pertLevel)


printTable(stats, "introduced_per_sample")
