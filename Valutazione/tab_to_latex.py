import json

with open("./tab_values.json") as f:
    vals = json.load(f)


bert = vals["Bert"]
pgp = vals["Pgp"]

for key in bert.keys():
    bert_cpp = str(round(bert[key]["corrected_per_perturbation"], 2))
    bert_ips = str(round(bert[key]["introduced_per_sample"], 2))
    bert_ipc = str(round(bert[key]["introduced_per_corrected"], 2))
    pgp_cpp = str(round(pgp[key]["corrected_per_perturbation"], 2))
    pgp_ips = str(round(pgp[key]["introduced_per_sample"], 2))
    pgp_ipc = str(round(pgp[key]["introduced_per_corrected"], 2))
    print(f"{key} & {bert_cpp} & {pgp_cpp} & {bert_ips} & {pgp_ips} & {bert_ipc} & {pgp_ipc} \\\\")
