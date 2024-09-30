import string
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as c
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import squarify
import pandas as pd
from matplotlib.lines import Line2D

from dataVisualization import label_formatter

plt.rcParams['font.family'] = 'Arial'
CHART_WIDTH_FULL = 11.18
CHART_WIDTH_HALF = 5.51
CHART_WIDTH_TWO_THIRDS = 8.28
CHART_HEIGHT = 4.79
special_chars = [' ', '\n', '&', '-', 'ē', 'é', '.', "'", 'ä']
_char_length = {}


def _label_width(label:str, fontsize) -> float:
    """
    get the width of the matplotlib.text.Text object with the given label
    e.g. "7,250" = 12.23 + 6.25 + 12.25 + 12.25 + 12.375 = 55.375
    :param label: the label value to be measured
    :return: the width of the label as a floating point number
    """
    # an empty dict returns false, we can check if our dict has content below if not we add content
    if not _char_length:
        renderer = plt.gcf().canvas.get_renderer()
        for i in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) + special_chars:
            my_num = plt.text(0, 0, i, size=fontsize, family='Arial')
            _char_length[i] = {"height": my_num.get_window_extent(renderer=renderer).height,
                        "width": my_num.get_window_extent(renderer=renderer).width}
            my_num.remove()

    length = 0.0
    for char in label:
        length = length + _char_length[char]["width"]
    return length


def _label_height(label:str, fontsize) -> float:
    """
    get the width of the matplotlib.text.Text object with the given label
    e.g. "7,250" = 12.23 + 6.25 + 12.25 + 12.25 + 12.375 = 55.375
    :param label: the label value to be measured
    :return: the width of the label as a floating point number
    """
    # an empty dict returns false, we can check if our dict has content below if not we add content
    if not _char_length:
        renderer = plt.gcf().canvas.get_renderer()
        for i in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) + special_chars:
            my_num = plt.text(0, 0, i, size=fontsize, family='Arial')
            _char_length[i] = {"height": my_num.get_window_extent(renderer=renderer).height,
                        "width": my_num.get_window_extent(renderer=renderer).width}
            my_num.remove()

    height = 0.0
    print(label)
    for char in label:
        if _char_length[char]["height"] > height:
            height = _char_length[char]["height"]
        if char == '\n':
            height = height * 2
        # height = height + _char_length[char]["height"]
    return height


def make_treemap(dataframe: pd.DataFrame, format: pd.DataFrame):
    my_values = dataframe['ESG %'].values
    print(my_values)

    colors_li=["#FFFFFF", "#F4DBAA", "#EDC371", "#EAB755", "#E6AB39", "#E39F1C", "#DF9300", "#EF7C10", "#FF641F"]
    legend_labels=['less than 10%', '10%-19%', '20%-29%', '30%-39%', '40%-49%', '50%-59%', '60%-69%', '70%-79%', '80%-89%', '90%-100%']


    colors = []
    for v in my_values:
        if v == 0:
            colors.append(colors_li[0])
        elif 0 <= v < 0.1:
            colors.append(colors_li[1])
        elif 0.1 <= v < 0.2:
            colors.append(colors_li[2])
        elif 0.2 <= v < 0.3:
            colors.append(colors_li[3])
        elif 0.3 <= v < 0.4:
            colors.append(colors_li[4])
        elif 0.4 <= v < 0.5:
            colors.append(colors_li[5])
        elif 0.5 <= v < 0.6:
            colors.append(colors_li[6])
        elif 0.6 <= v < 0.7:
            colors.append(colors_li[7])
        elif 0.7 <= v <= 1.0:
            colors.append(colors_li[8])
        else:
            colors.append("#000000")
    labels = []

    # plot it
    squarify.plot(sizes=dataframe['Followers'], color=colors, edgecolor='#98989c', linewidth=0.5)
    plt.axis('off')

    labels = dataframe['Corporate'].values.tolist()
    label_pairs = []
    for index, container in enumerate(plt.gca().containers):
        for j in range(len(labels)):
            rect = container[j]
            label_formatter.format_label(plt.gca(), rect, labels[j], format)


    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=legend_labels[i], markerfacecolor=colors_li[i], markersize=15) for i in range(len(legend_labels)-2)
    ]

    if format["Legend"].lower().strip().strip() == "yes":
        axins = inset_axes(
            plt.gca(),
            width="5%",  # width: 5% of parent_bbox width
            height="30%",  # height: 30%
            loc="lower right",
            bbox_to_anchor=(0, -0.07, 1, 1),
            bbox_transform=plt.gca().transAxes,
            borderpad=0,
        )

        cbar = plt.gcf().colorbar(cm.ScalarMappable(
            cmap=c.ListedColormap(colors_li)),
            cax=axins,
            # location='bottom',
            aspect=10,
            shrink=0.35,
            ticks=[0, 1],
            orientation='horizontal'
        )
        cbar.ax.set_xticklabels(['0%', '100%'])

    if format['Chart Size'].lower().strip().strip() == 'full':
        ratio = 0.55
        plt.gcf().set_figwidth(CHART_WIDTH_FULL, True)
    elif format['Chart Size'].lower().strip().strip() == 'half':
        ratio = 1.2
        plt.gcf().set_figwidth(CHART_WIDTH_HALF, True)
    elif format['Chart Size'].lower().strip().strip() == 'two thirds':
        ratio = 0.5254
        plt.gcf().set_figwidth(CHART_WIDTH_TWO_THIRDS, True)
    plt.gcf().set_figheight(CHART_HEIGHT, True)

    plt.gca().set(xmargin=0.5)
    plt.gca().set_frame_on(False)
    # plt.gcf().set_size_inches(CHART_WIDTH_HALF,CHART_HEIGHT)

    x_left, x_right = plt.gca().get_xlim()
    y_low, y_high = plt.gca().get_ylim()
    plt.gca().set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    return plt.gcf()
