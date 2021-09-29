import string
from itertools import chain
from detokenize import detokenize
from nltk import word_tokenize
from random import shuffle
import json
from nltk import data
from tqdm import tqdm
import sys
# yapf: disable
sys.path.insert(0, "../../../Perturbazione")
sys.path.insert(0, "../")
# yapf: enable
from pipeline import replaceTokens
from bert_filler import Filler

VOCAB_FILE = "../lexicon.txt"
FINAL_DATASET_FILE = "../../../Creazione_Dataset/dataset_v2f.json"
OUTPUT_FILE = "errorstudy_dataset.json"
MIN_LEN = 40

DATASET_COMPOSITION = {
    "text": 3500,
    "M1": 3500,
    "M2": 3500,
    "M3": 3500,
    "S1": 3500,
    "S2": 3500,
    "S3": 3500,
    "T1": 3500,
    "T2": 3500,
    "T3": 3500
}

QUOTES = (
    '\u0022'  # "
    '\u0027'  # '
    '\u2018'  # ‘
    '\u2019'  # ’
    '\u201b'  # ‛
    '\uff07'  # ＇
)

print("Eseguendo il setup dello script, non ci vuole tanto :)")

alternatives_dict = {}
with open("../../../Perturbazione/submatrix_extraction/confusionMatrix.json"
          ) as f:
    subData = json.load(f)

# Leggendo il dataset
with open(FINAL_DATASET_FILE) as f:
    dataset = json.load(f)

# Leggendo il dizionario
vocabulary = set()
with open(VOCAB_FILE) as f:
    for line in f:
        vocabulary.add(line.strip())
for punct in string.punctuation:
    vocabulary.add(punct)

bert_filler = Filler()

# Appiattendo dataset
# Il dataset sarà ora un insieme di 10 liste di frasi, ognuna delle quali conterrà
# tutte le frasi estratte con un singolo metodo di perturbazione

dataset = [{"text": x["text"], **x["perturbed"]} for x in dataset]

dataset_new = {key: [] for key in dataset[0].keys()}
for i in range(len(dataset)):
    element = dataset.pop()
    for key in dataset_new.keys():
        if len(element[key]) >= MIN_LEN:
            dataset_new[key].append(element[key])

for key in dataset_new.keys():
    shuffle(dataset_new[key])

dataset = dataset_new

# Scegliendo frasi a campione
dataset_list = []
for key in DATASET_COMPOSITION:
    extension = dataset[key][:DATASET_COMPOSITION[key]]
    extension = [{"sent": e, "pert_level": key} for e in extension]
    dataset_list.extend(extension)


def isTokenCorrect(words: str, index: int) -> bool:
    if len(words[index]) <= 1:
        return False
    if words[index].lower() in vocabulary:
        return True
    # Checking if error word is a word with apostrophe
    if index + 1 < len(words) and words[index + 1] in QUOTES:
        word = words[index]
        possibleFull = [word.lower() + c for c in ["a", "e", "i", "o", "u"]]
        return any([p in vocabulary for p in possibleFull])
    return False


def perturbed(token: str):
    return replaceTokens(token, subData, alternatives_dict, 5)


def recomposeSentece(tokens, maskIndex, subToken):
    sent_tokens = [
        token if index != maskIndex else subToken
        for index, token in enumerate(tokens)
    ]
    sentece = detokenize(sent_tokens)
    return sentece


def produce_datapoints(sentence: str, pert_level: str):
    tokens = word_tokenize(sentence)
    correct_list = []

    for index, token in enumerate(tokens):
        if isTokenCorrect(tokens, index):
            correct_list.append(index)

    if len(correct_list) == 0:
        return []

    shuffle(correct_list)
    chosen_token_index = correct_list[0]
    chosen_token = tokens[chosen_token_index]

    perturbed_token = chosen_token
    counter = 0
    while (perturbed_token == chosen_token):
        perturbed_token = perturbed(chosen_token)
        counter += 1
        if counter == 10:
            return None

    datapoint = {
        "sentence": recomposeSentece(tokens, chosen_token_index, "[MASK]"),
        "masked_word": perturbed_token,
        "correct_word": chosen_token,
        "pert_level": pert_level
    }
    return datapoint


dataset_list = [
    produce_datapoints(x["sent"], x["pert_level"])
    for x in tqdm(dataset_list, desc="Producendo perturbazioni controllate")
]
dataset_list = [x for x in dataset_list if x != None]

with open(OUTPUT_FILE, "w") as f:
    json.dump(dataset_list, f, indent=2)