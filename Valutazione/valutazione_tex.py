import json
from plot_results import calculateVals


def printStat(vals: dict, stat: str):
    vals_c = {project: {pert_level: stats[stat] for pert_level, stats in val.items()}
              for project, val in vals.items()}
    out = ""
    pert_levels = list(vals_c[list(vals_c.keys())[0]].keys())
    out += " "
    for lev in pert_levels:
        out += " & " + "\\textbf{" + lev + "}"
    out += "\\\\ \\hline \n"

    for project, val in vals_c.items():
        out += project
        for pert_level, stat_p in val.items():
            out += " & " + "{:.3f}".format(stat_p)
        out += "\\\\ \n"
    print(out)


with open("./valutazione_tot.json") as f:
    vals = json.load(f)

vals = calculateVals(vals)
printStat(vals, "corrected_per_perturbation")
