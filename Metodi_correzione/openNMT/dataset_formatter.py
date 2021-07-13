import json

with open('../../Creazione_Dataset/dataset_reduced.json') as data_file:
    dataset = json.load(data_file)


#function that takes a string a sub the spaces with #
def sub_spaces(string):
    string = string.replace(" ", "#")
    string = " ".join([c + " " for c in string]).strip()
    return string


keys = list(dataset[0]["perturbed"].keys())

for key in keys:
    sentenceList = []
    for datapoint in dataset:
        formatted_sentence = sub_spaces(datapoint["perturbed"][key])
        sentenceList.append(formatted_sentence)
    with open(f"./targets/{key}.tgt", "w") as f:
        for sentence in sentenceList:
            f.write(sentence + "\n")

sentenceList = []
for datapoint in dataset:
    sentence = sub_spaces(datapoint["text"])
    sentenceList.append(sentence)

with open("./original.src", "w") as f:
    for sentence in sentenceList:
        f.write(sentence + "\n")
