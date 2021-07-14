import json
from os import write
from random import shuffle

validation_size = 5000

print("Leggendo il dataset")
with open('../../Creazione_Dataset/dataset.json') as data_file:
    dataset = json.load(data_file)

print("Mescolando il dataset")
shuffle(dataset)

validation = dataset[:validation_size]
dataset = dataset[validation_size:]


#function that takes a string a sub the spaces with #
def sub_spaces(string):
    string = string.replace(" ", "#")
    string = " ".join([c for c in string]).strip()
    return string


# Write the dataset to files
def write_files(dataset, folderName):
    keys = list(dataset[0]["perturbed"].keys())
    for key in keys:
        sentenceList = []
        for datapoint in dataset:
            formatted_sentence = sub_spaces(datapoint["perturbed"][key])
            sentenceList.append(formatted_sentence)
        with open(f"./{folderName}/{key}.tgt", "w") as f:
            for sentence in sentenceList:
                f.write(sentence + "\n")


def write_files_original(dataset, folderName):
    sentenceList = []
    for datapoint in dataset:
        sentence = sub_spaces(datapoint["text"])
        sentenceList.append(sentence)

    with open(f"./{folderName}/original.src", "w") as f:
        for sentence in sentenceList:
            f.write(sentence + "\n")


write_files_original(dataset, "train")
write_files_original(validation, "test")
write_files(dataset, "train")
write_files(validation, "test")
