import json
from os import remove
from tqdm import tqdm

# Carattere che sostituisce lo spazio nella sequenza di output
spaceSub = "##"
inCorpusName = "dataset.input"
outCorpusName = "dataset.output"


def removeDoubleSpaces(string):
    # Normalizza tutti gli spazi bianchi come tab ecc a un singolo " "
    return " ".join(string.split())


def trainInput(sample):
    sample = removeDoubleSpaces(sample)
    sample = [char + " " for char in sample if char != " "]
    sample = "".join(sample)
    return sample


def trainOutput(sample):
    sample = removeDoubleSpaces(sample)
    sample = sample.replace(" ", spaceSub)
    return sample


with open("./extracted.json") as f:
    samples = json.load(f)

samples = [(trainInput(sample), trainOutput(sample))
           for sample in tqdm(samples, "Producendo le coppie di campioni")]

print("Sto generando i datasets...")
with open(inCorpusName, 'w') as inFile, open(outCorpusName, 'w') as outFile:
    inLines, outLines = zip(*samples)
    inFile.writelines([line + "\n" for line in inLines])
    outFile.writelines([line + "\n" for line in outLines])

print(
    f"Fatto! I file {inCorpusName} e {outCorpusName} sono stati creati nella directory corrente")


# TODO: genero uno split per il test set
