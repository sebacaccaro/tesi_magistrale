import json
import matplotlib.pyplot as plt
import pandas as pd

fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 7
fig_size[1] = 10


def codeConvert(code):
    return {
        key: {
            **x,
            "corrected_per_perturbation":
            x["corrected_errors"] / x["perturbation_errors"],
            "introduced_per_sample":
            x["introduced_errors"] / x["total_chars"],
            "introduced_per_corrected":
            x["introduced_errors"] / x["corrected_errors"],
        }
        for key, x in code.items()
    }


def calculateVals(vals):
    return {key: codeConvert(value) for key, value in vals.items()}


def plottable_sub_dict(dict_to_plot: dict, stat_to_plot: str) -> dict:
    return {
        key: value[stat_to_plot]
        for key, value in sorted(dict_to_plot.items())
    }


def plottable_dict(dict_to_plot: dict, stat_to_plot: str) -> dict:
    return {
        key: plottable_sub_dict(dict_int, stat_to_plot)
        for key, dict_int in dict_to_plot.items()
    }


""" def plot_dict(subPlot, D: dict, title):
    color = ['#1B4E6B', '#1B4E6B', '#1B4E6B', '#5C63A2', '#5C63A2',
             '#5C63A2', '#C068A8', '#C068A8', '#C068A8']
    last_D = None

    i = 0
    for project, sub_D in D.items():
        print("a")
        last_D = sub_D
        subPlot.bar([x+i for x in range(len(sub_D))], list(sub_D.values()),
                    align='center', color=color, width=0.2)
        i += 1

    subPlot.set_xticks(range(len(last_D)*2))
    subPlot.set_xticklabels(list(last_D.keys()))
    subPlot.title.set_text(title)
    add_value_labels(subPlot, -15) """


def bar_plot(ax,
             data,
             colors=None,
             total_width=0.8,
             single_width=1,
             legend=False,
             bar_offset=1):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.

    bar_offset: float, optional, default = 1
        Set to center the lines.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = ((i - n_bars / 2) * bar_width +
                    bar_width / 2) + bar_offset * bar_width

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset,
                         y,
                         width=bar_width * single_width,
                         color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys(), loc='lower center')
        # Shrink current axis's height by 10% on the bottom
        """ box = ax.get_position()
        ax.set_position(
            [box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

        # Put a legend below current axis
        ax.legend(bars,
                  data.keys(),
                  loc='upper center',
                  bbox_to_anchor=(0.5, -0.05),
                  fancybox=True,
                  ncol=5) """


def plot_dict(subPlot, D: dict, title):
    df = pd.DataFrame(D)
    bar_plot(subPlot, df, single_width=1, total_width=0.8, bar_offset=2.5)
    subPlot.set_xticks(range(len(df.index)))
    subPlot.set_xticklabels(df.index)
    subPlot.title.set_text(title)
    print(
        "Se il grafico non è centrato, gioca con il parametro bar:offset nella funzione plot_dict"
    )


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
            label,  # Use `label` as label
            (x_value, y_value),  # Place label at end of the bar
            xytext=(0, space),  # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',  # Horizontally center label
            color="white",
            va=va)  # Vertically align label differently for
        # positive and negative values


if __name__ == "__main__":
    with open("./valutazione_2.json") as f:
        val = json.load(f)

    val = calculateVals(val)

    with open("tab_values.json", "w") as f:
        json.dump(val, f, indent=2)

    gp = val

    figure, axes = plt.subplots(nrows=5, ncols=1)

    axNum = 0

    plot_dict(axes[axNum], plottable_dict(gp, "corrected_per_perturbation"),
              "Errori corretti per errore di perturbazione introdotto")

    axNum += 1
    plot_dict(axes[axNum], plottable_dict(gp, "introduced_per_sample"),
              "Errori introdotti per frase")
    axNum += 1

    plot_dict(axes[axNum], plottable_dict(gp, "introduced_per_corrected"),
              "Errori introdotti per errore corretto")
    axNum += 1

    plot_dict(axes[axNum], plottable_dict(gp, "lev_reduction_per_sentence"),
              "Riduzione della distanza di Levenshtein")
    axes[axNum].axhline(0, color='black', linewidth=1)
    axNum += 1

    plot_dict(axes[axNum], plottable_dict(gp, "total_distance_per_char"),
              "Distanza di Levenshtein totale")
    axes[axNum].axhline(0, color='black', linewidth=1)
    axNum += 1

    plt.subplots_adjust(top=0.95,
                        bottom=0.045,
                        left=0.1,
                        right=0.98,
                        hspace=0.375,
                        wspace=0.185)

    plt.savefig("Valutazione.png")
    plt.show()
