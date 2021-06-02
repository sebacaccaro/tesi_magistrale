import json
from tqdm import tqdm
from Levenshtein import distance, matching_blocks, editops

with open("./ocr_corrections.json") as f:
    corrections = json.load(f)


def invert(dict):
    newDict = {}
    for key, value in tqdm(dict.items(), "Invertendo dizionario"):
        if not value in newDict.keys():
            newDict[value] = []
        if distance(key, value) < 3:
            newDict[value].append(key)

    return newDict


def extractPair(correctw, incorrectw):
    matching = matching_blocks(
        editops(correctw, incorrectw), correctw, incorrectw)
    correctw = [c for c in correctw]
    incorrectw = [c for c in incorrectw]
    for mb in matching:
        for i in range(mb[0], mb[0]+mb[2], 1):
            correctw[i] = None
        for i in range(mb[1], mb[1]+mb[2], 1):
            incorrectw[i] = None
    correctw = "".join([c for c in correctw if c])
    incorrectw = "".join([c for c in incorrectw if c])
    return(correctw, incorrectw)


def extractMatrix(mistakes_pairs):
    confMatrix = {}
    for correct_word, misspelled_words in tqdm(list(mistakes_pairs.items()), "Creando la confusion misspelling matrix"):
        for misspelled_word in misspelled_words:
            original_chars, mistaken_chars = extractPair(
                correct_word, misspelled_word)
            if not original_chars in confMatrix:
                confMatrix[original_chars] = {}
            if not mistaken_chars in confMatrix[original_chars]:
                confMatrix[original_chars][mistaken_chars] = 0
            confMatrix[original_chars][mistaken_chars] += 1
    return confMatrix


def filterByFrequency(conf_matrix, threshold):
    for original_char, mistaken_chars_dict in conf_matrix.items():
        new_freq = {}
        for mistaken_char, count in mistaken_chars_dict.items():
            if count >= threshold:
                new_freq[mistaken_char] = count
        conf_matrix[original_char] = new_freq
    keys_to_delete = []
    for original_char in conf_matrix:
        if len(conf_matrix[original_char]) < 1:
            keys_to_delete.append(original_char)
    for key in keys_to_delete:
        del(conf_matrix[key])


inverted = invert(corrections)
confMatrix = extractMatrix(inverted)
filterByFrequency(confMatrix, 7)

count = {orig_char: sum(sub_dict.values())
         for orig_char, sub_dict in confMatrix.items()}

output = {
    "subs": confMatrix,
    "count": count
}


with open("confusionMatrix.json", "w") as f:
    json.dump(output, f, indent=2)
