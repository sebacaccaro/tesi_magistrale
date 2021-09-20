import json
from tqdm import tqdm

EXTRACED_SENTENCES_FILE = "../../../Creazione_Dataset/extracted.json"
FINAL_DATASET_FILE = "../../../Creazione_Dataset/dataset_v2f_reduced.json"
OUTPUT_FILE = "train_set.json"

MIN_LEN = 20

print("Leggendo tutte le frasi estratte")
with open(EXTRACED_SENTENCES_FILE) as f:
    extraced_senteces = json.load(f)

print("Leggendo il dataset su cui si faranno i test")
with open(FINAL_DATASET_FILE) as f:
    final_dataset = json.load(f)


def isSameEntry(entry1, entry2):
    return (entry1["docnum"] == entry2["docnum"] and
            entry1["parId"] == entry2["parId"] and
            entry1["parPos"] == entry2["parPos"])


def isEntryInDataset(entry: dict, dataset: list):
    for dataset_entry in dataset:
        if isSameEntry(dataset_entry, entry):
            return True
    return False


def isFirstParagraph(fragment):
    return fragment["parId"] == 0


def isLastParagraph(fragment, maxes):
    return fragment["parId"] == maxes[fragment["docnum"]]


intial_len = len(extraced_senteces)

extraced_senteces[:] = [
    entry for entry in tqdm(extraced_senteces) if not isEntryInDataset(entry, final_dataset)]

discarded_num = intial_len - len(extraced_senteces)

print(f"Sono state scartate {discarded_num} frasi.")


# Ora filtro i paragrafi che non voglio
docs = set([x["docnum"] for x in tqdm(extraced_senteces)])
maxes = {}

print("Filtrando le frasi per paragrafo...")
for fragment in extraced_senteces:
    if fragment["docnum"] not in maxes:
        maxes[fragment["docnum"]] = []
    maxes[fragment["docnum"]].append(fragment["parId"])

maxes = {docnum: max(maxList) for docnum, maxList in tqdm(maxes.items())}

extraced_senteces = [f["text"] for f in tqdm(extraced_senteces) if not (
    isFirstParagraph(f) or isLastParagraph(f, maxes) or len(f["text"]) < MIN_LEN)]

print(f"Scrivendo il train_set in {OUTPUT_FILE} ....")
with open(OUTPUT_FILE, "w") as f:
    json.dump(extraced_senteces, f, indent=2)
