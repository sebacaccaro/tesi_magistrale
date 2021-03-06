import json
import os
from tqdm import tqdm
from itertools import chain
from nltk.tokenize import sent_tokenize
import nltk
nltk.download('punkt')

#### CONFIG ####
dataset_folder = "../../Dataset/vatpub/"
languages = ["it"]
out_file = "sentences.json"


def fileToData(filename):
    with open(dataset_folder + filename) as f:
        return json.load(f)


def paragraphListEnriched(fileNum, paragraphList):
    return [{"text": p, "docnum": fileNum, "parId": i, "parPos": 0} for i, p in enumerate(paragraphList)]


##### MAIN ####
fileNames = sorted(list(os.listdir(dataset_folder)))

# Leggendo i files
files = {int(fileName.replace(".json", "")): fileToData(fileName)
         for fileName in tqdm(fileNames, "Leggendo i file")}
# Tengo solo quelli nelle lingue scelta
files = {fileNumber: file for fileNumber,
         file in files.items() if file["language"] in languages}
# Tengo solo i campi paragraph_text e li divido in frasi
files = {fileNumber: file["paragraphs"]
         for fileNumber, file in files.items()}

files = {fileNumber: [paragraph["text"] for paragraph in file]
         for fileNumber, file in tqdm(files.items(), "Dividendo i paragrafi in frasi")}

files = {fileNumber: paragraphListEnriched(
    fileNumber, pList) for fileNumber, pList in files.items()}

print(f"Salvando le frasi in {out_file}...")
with open(out_file, "w") as f:
    json.dump(files, f, indent=2)
print(f"{out_file} scritto con successo ;)")
