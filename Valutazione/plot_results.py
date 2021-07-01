import json
import matplotlib.pyplot as plt

fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 7
fig_size[1] = 10

with open("./valutazione.json") as f:
    val = json.load(f)

gp = val["project_gender_politcs"]

gp = {key: {
    **x,
    "corrected_per_perturbation": x["corrected_errors"]/x["perturbation_errors"],
    "introduced_per_sample": x["introduced_errors"]/x["total_samples"],
    "introduced_per_corrected": x["introduced_errors"]/x["corrected_errors"],
} for key, x in gp.items()}


def plottable_dict(dict_to_plot: dict, stat_to_plot: str) -> dict:
    return {key: value[stat_to_plot] for key, value in dict_to_plot.items()}


def plot_dict(subPlot, D: dict, title):
    color = ['#1B4E6B', '#1B4E6B', '#1B4E6B', '#5C63A2', '#5C63A2',
             '#5C63A2', '#C068A8', '#C068A8', '#C068A8']
    subPlot.bar(range(len(D)), list(D.values()), align='center', color=color)
    subPlot.set_xticks(range(len(D)))
    subPlot.set_xticklabels(list(D.keys()))
    subPlot.title.set_text(title)
    add_value_labels(subPlot, -15)


def add_value_labels(ax, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        label = "{:.3f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            color="white",
            va=va)                      # Vertically align label differently for
        # positive and negative values


figure, axes = plt.subplots(nrows=3, ncols=1)


plot_dict(axes[0], plottable_dict(gp, "corrected_per_perturbation"),
          "Errori corretti per errore di perturbazione introdotto")
plot_dict(axes[1], plottable_dict(gp, "introduced_per_sample"),
          "Errori introdotti per frase")
plot_dict(axes[2], plottable_dict(gp, "introduced_per_corrected"),
          "Errori introdotti per errore corretto")
plt.subplots_adjust(top=0.95,
                    bottom=0.045,
                    left=0.1,
                    right=0.98,
                    hspace=0.375,
                    wspace=0.185)

plt.savefig("Valutazione.png")
plt.show()
