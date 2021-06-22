import os
import json

eval_folder = "./dataset_valutati"
out_file = "valutazione.json"

correction_folders = {
    "project_gender_politics": "../Metodi_correzione/project_gender_politics/corrections/"
}

blackList = [
    "errors_",
    ".md"
]


def blackListed(filename):
    return any([x in filename for x in blackList])


def corrected_errors(datapoint):
    return 0


def inserted_errors(datapoint):
    return 0


def original_errors(datapoint):
    return 0


def evalCorrection(correction_set):
    def prefix_str(
        x): return f"({correction_set['project']}-{correction_set['pert_level']}) {x}"

    print(prefix_str("Leggendo il dataset..."))
    with open(correction_set["path"]) as f:
        dataset = json.load(f)
    print(prefix_str("Calcolando gli errori..."))
    for datapoint in dataset:
        datapoint["original_errors"] = original_errors(datapoint)
        datapoint["corrected_errors"] = corrected_errors(datapoint)
        datapoint["inserted_errors"] = inserted_errors(datapoint)

    print(prefix_str("Salvando il dataset con le correzioni..."))
    with open(f"{eval_folder}/{correction_set['project']}_{correction_set['pert_level']}.json", "w") as f:
        json.dump(dataset, f, indent=2)

    return {
        **correction_set,
        "errors_stats": {
            "original_errors": sum([d["original_errors"] for d in dataset]),
            "corrected_errors": sum([d["corrected_errors"] for d in dataset]),
            "inserted_errors": sum([d["inserted_errors"] for d in dataset]),
        }
    }


folders_files = {project:
                 [{"path": folder + file, "pert_level": file.replace(".json", ""), "project": project}
                     for file in os.listdir(folder) if not blackListed(file)]
                 for project, folder in correction_folders.items()}


evaluations = {
    project: [evalCorrection(correction) for correction in corrections]
    for project, corrections in folders_files.items()
}

with open(out_file, "w") as f:
    json.dump(evaluations, f, indent=2)

print(f"I risultati sono stati valutati, output scritto in {out_file}")
