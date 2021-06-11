from re import finditer
import json
from itertools import chain

with open("sentences.json") as f:
    sentences = json.load(f)
sentences = {int(key): value for key, value in sentences.items()}

##### CONFIG #####
doc_min = 0
doc_max = max(sentences.keys())

min_len = 8  # Minum accetable length for a sentence
max_len = 50  # Maximum accetable length for a sentence
def accettable_length(sent): return min_len <= len(sent) <= max_len


output_filename = "extracted.json"
######################


def fallbackSplit(sentence, max_optimal_size):
    """ Chop of the sentece string in string of max_optimal_size and the rest """
    if len(sentence) <= max_optimal_size:
        return sentence, None
    return sentence[:max_optimal_size], sentence[max_optimal_size:]


def numSplit(sentence, max_optimal_size):
    """ Divide the string into an optimal size based on numebers """
    splitPositions = [match.span()[0] for match in finditer(
        r"(?<![a-zA-Z:])\d*\.?\d+", sentence)]
    splitPoints = sorted([x for x in splitPositions if x <= max_optimal_size])
    print(splitPoints)
    if len(splitPoints) == 0 or splitPoints[-1] == 0:
        return fallbackSplit(sentence, max_optimal_size)
    splitPoint = splitPoints[-1]
    return sentence[:splitPoint], sentence[splitPoint:]


def smartSplit(sentence, max_optimal_size=max_len):
    """ Divide the string into a optimal dataset string and the rest

    Parameters:
    sentece (str): sentece to be split
    max_optimal_size (int): upper limit for return lenght, and optimal size to reach

    Returns:
    optimal_str (str): optimal string to be added to the dataset
    rest_str (str): rest of the string
    """
    if(len(sentence) <= max_optimal_size):
        return sentence, None
    punktMarks = ["?", "!", ";", ":"]
    splitPoints = [str.find(sentence, punktMark) for punktMark in punktMarks]
    if all([x == -1 or x >= max_optimal_size for x in splitPoints]):
        return numSplit(sentence, max_optimal_size)
    splitPoint = sorted(
        [x for x in splitPoints if x <= max_optimal_size])[-1] + 1
    return sentence[:splitPoint], sentence[splitPoint:]


allsentences = list(chain(*sentences.values()))
sent_number = len(allsentences)
extracted = [phr for phr in allsentences if accettable_length(phr)]

allsentences = [phr for phr in allsentences if not accettable_length(phr)]


print(f"Numero totali di frasi nel dataset: {sent_number}")
print(f"Splittando frasi in sequenze da max {max_len} caratteri")

while len(allsentences) > 0:
    if len(extracted) % 1000 == 0:
        print(
            f"Frasi da elaborare: {len(allsentences)} -- Frasi Prodotte: {len(extracted)}")
    extracted_sent, rest = smartSplit(allsentences.pop(0))
    extracted.append(extracted_sent)
    if(rest):
        allsentences.append(rest)

extracted = [x for x in extracted if accettable_length(x)]

with open(output_filename, "w") as f:
    json.dump(extracted, f, indent=2)
"""  
Da 

Nastase, V., & Hitschler, J. (2018, May). 
Correction of OCR word segmentation errors in articles from the ACL collection through neural machine translation methods.
In Proceedings of the Eleventh International Conference on Language Resources and Evaluation (LREC 2018).


......the texts with one paragraph per line are split into
smaller fragments, avoiding as much as possible split-
ting on ”ambiguous” breaking points (i.e. spaces be-
tween text fragments which may actually be erro-
neous):
(a) split on end of sentence characters or phrase de-
limiting characters (.?!;: - parentheses)
(b) if the fragment is longer than 50 characters, split
at numbers
(c) if the fragment is still longer than 50 characters,
split into 50 character long sequences
 """
