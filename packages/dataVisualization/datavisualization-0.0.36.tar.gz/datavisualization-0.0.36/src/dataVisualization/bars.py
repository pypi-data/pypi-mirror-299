"""
This file handles the creation of bar plots for the data-visualisation project
Produces png graphs to designated folder
Is typically called from dataVisualization.py
"""
import math
import string
from typing import Callable, List

import pandas as pd
import matplotlib.container as con
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.container as container
import matplotlib.cm as cm
import matplotlib.colors as c
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.lines import Line2D
import numpy as np
from sklearn.linear_model import Ridge

import dataVisualization.susmon_colours as sc
import dataVisualization.vis_scripts as vs

from adjustText import adjust_text
from faker import Faker
from palmerpenguins import load_penguins

#import src.main.susmon_colours as sc

# CONSTANTS:
LEGEND_Y_POS = -5.5
BARWIDTH = 0.75
CHART_WIDTH_FULL = 11.18
CHART_WIDTH_HALF = 5.51
CHART_HEIGHT = 4.79
CHART_HEIGHT_PORTRAIT = 8
DECIMAL_PLACES = 2 # how many decimal places to be used if value is more than 1,000,000
FONT_WEIGHT = 'normal'

#Variables
_char_length = {}
special_chars = [' ', '\n', '&', '-', 'ē', 'é', '.', "'", 'ä', '(', ')', 'ò', '/', 'ë', 'è', 'ö']


def _get_data_cols(dataframe: pd.DataFrame) -> list[str]:
    """
    Takes a given dataframe and returns the names of data columns,
    these are the columns with data used to make the bars.
    The dataframe should be in te following format:
    Subject | data_cols* | Total | optional cols | ect.
    where data_cols is a variable number of cols that names will be returned
    :param dataframe: the dataframe we want to get the cols from
    :return:
    """
    # get the data column names
    cols = dataframe.columns.tolist()
    cols.pop(0)  # remove the Subject col
    for i in range(0, len(cols) - cols.index('Total')):
        # remove the Total col and all cols after it
        # leaving just the data cols
        cols.pop()
    return cols


def _format_func_gen(magnitude: int) -> Callable:
    """
    Generate a formatting function to pass to FuncFormatter used to format X-ticks
    Depending on the scale of the chart we would need to pass different functions to FuncFormatter
    (one for thousands, one for millions ect.) Rather than manually writing multiple functions with repeated code
    we generate the correct function at runtime.
    :param magnitude: This is the scale of the largest number in the chart calculated as floor(log(highest_val, 1000))
    :return: formatting function
    """

    def inner(num: float, _pos: int) -> str:
        return '{:,.6g}{}'.format(num / (1000 ** magnitude), ['', 'k', 'm', 'bn', 'tn'][magnitude])

    return inner


def _generate_bars(dataframe: pd.DataFrame, fmt: pd.Series, colorList: list[str]):
    """
    Loops through the cols in a given dataframe to automatically generate a list
    of bar objects
    :param dataframe: A DataFrame that contains the data to be turned in to bars
    :param format: A pd.Series that contains the data on how the chart should be presented
    :param colorList: a list of color strings used to color the bars
    :return: returns a Figure of the plot
    """
    # get the data column names
    cols = _get_data_cols(dataframe)
    if fmt['Chart Type'].lower() == 'esg trend bar':
        del cols[0]
        print(cols)

    if 'Followers' in cols:
        plt.gca().set_xscale('log')

    # generate the bars
    if fmt['Chart Type'].lower() != 'esg trend bar':
        acc = 0
        for i in range(len(cols)):
            bar = dataframe[cols[i]].values.tolist()
            print(bar)
            plt.barh(range(len(bar)),
                     bar,
                     color=colorList[i],
                     left=acc,
                     edgecolor='none',
                     height=BARWIDTH,
                     zorder=3)
            acc = np.add(acc, bar)

            plt.yticks(range(len(dataframe[cols[i]].values.tolist())), dataframe.iloc[:,0].values.tolist())
        plt.xlim(0, np.array(acc).max())
    else:
        acc = 0
        for i in range(len(cols)):
            bar = dataframe[cols[i]].values.tolist()
            print(bar)
            plt.bar(range(len(bar)),
                     bar,
                     color=colorList[i],
                     bottom=acc,
                     edgecolor='none',
                     width=BARWIDTH,
                     zorder=3)
            acc = np.add(acc, bar)

            plt.yticks(range(len(dataframe[cols[i]].values.tolist())), dataframe.iloc[:, 0].values.tolist())
        plt.ylim(0, np.array(acc).max())


def _label_width(label:str) -> float:
    """
    get the width of the matplotlib.text.Text object with the given label
    e.g. "7,250" = 12.23 + 6.25 + 12.25 + 12.25 + 12.375 = 55.375
    :param label: the label value to be measured
    :return: the width of the label as a floating point number
    """
    # an empty dict returns false, we can check if our dict has content below if not we add content
    if not _char_length:
        renderer = plt.gcf().canvas.get_renderer()
        for i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", ",", 'k', 'm', 'b', 't', '%']:
            my_num = plt.text(0, 0, i, size=8, family='Arial')
            _char_length[i] = {"height": my_num.get_window_extent(renderer=renderer).height,
                        "width": my_num.get_window_extent(renderer=renderer).width}
            my_num.remove()

    length = 0.0
    for char in label:
        length = length + _char_length[char]["width"]
    return length


def _make_q_ticks(dates: list):
    new_dates = []
    for d in range(len(dates)):
        if dates[d].month == 1:
            new_dates.append('Q1')
        elif dates[d].month == 4:
            new_dates.append('Q2')
        elif dates[d].month == 7:
            new_dates.append('Q3')
        elif dates[d].month == 10:
            new_dates.append('Q4')
        else:
            continue
    return new_dates


def _label_height(label:str) -> float:
    """
       get the height of the matplotlib.text.Text object with the given label
       e.g. "7,250" = 12.23 + 6.25 + 12.25 + 12.25 + 12.375 = 55.375
       :param label: the label value to be measured
       :return: the width of the label as a floating point number
       """
    # an empty dict returns false, we can check if our dict has content below if not we add content
    if not _char_length:
        renderer = plt.gcf().canvas.get_renderer()
        for i in list(string.ascii_lowercase + string.ascii_uppercase + string.digits) + special_chars:
            my_txt = plt.text(0, 0, i, size=6, family='Arial')
            _char_length[i] = {"height": my_txt.get_window_extent(renderer=renderer).height,
                               "width": my_txt.get_window_extent(renderer=renderer).width}
            my_txt.remove()

    height = 0.0
    for char in label:
        if _char_length[char]["height"] > height:
            print(char + " = " + str(_char_length[char]["height"]/6))
            height = _char_length[char]["height"]
        if char == '\n':
            print('double')
            height = height * 2
    print(height)
    return height / 6


def get_center(p1, p2):
    return (p2-p1)/2

def add_class_ticks(avgs, years, ax=plt.gca()):
    lbs = ax.get_xticklabels()
    locs = ax.get_xticks()
    sep_locs = []

    p1 = 0
    p2 = 0

    for i in range(len(lbs)):
        if lbs[i].get_text() == 'Q1' or i == 0:
            p1 = locs[i]
        elif lbs[i].get_text() == 'Q4' or i == len(lbs) - 1:
            p2 = locs[i]
            sep_locs.append(p1 + get_center(p1, p2))

    print('sep_locs: ', sep_locs)
    # label the classes:
    sec = ax.secondary_xaxis(location=0)
    sec.set_xticks(sep_locs, labels=years, fontweight='bold', color=sc.get_colour('non-sustainability'))
    sec.tick_params('x', length=0)
    for spine in sec.spines.values():
        spine.set_visible(False)


def add_seperator_lines(ax=plt.gca()):
    lbs = ax.get_xticklabels()
    locs = ax.get_xticks()
    sep_locs = []

    # get difference between ticks
    padding = (locs[1] - locs[0]) / 2

    for i in range(len(lbs)):
        if lbs[i].get_text() == 'Q4':
            sep_locs.append(locs[i] + padding)

    # lines between the classes:
    sec2 = ax.secondary_xaxis(location=0)
    sec2.set_xticks(sep_locs, labels=[])
    sec2.tick_params('x', length=30, width=0.375, colors='#A7A8AA')
    for spine in sec2.spines.values():
        spine.set_visible(False)

def divide_chunks(l, n):
    """
    split a list into n chunks
    :param l:
    :param n:
    """
    print('list', l)
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def chunk_avg(chunks):
    """
    get the average of each chunk
    :param chunks:
    :return:
    """
    avgs = []
    for chunk in chunks:
        avgs.append(sum(chunk) / len(chunk))
    return avgs


def chunk_maxi(chunks):
    """
    get the max of each chunk
    :param chunks:
    :return:
    """
    print("Chunks: ", chunks)
    maxis = []
    for chunk in chunks:
        maxis.append(max(chunk))
    print("Maxis: ", maxis)
    return (maxis)

def _get_segment_label_color(container:con.Container) -> str:
    """
    takes a given container and returns the correct color for it
    white is returned if the container is susmon dark grey
    black is returned in all other cases
    :param container: the container for this segment
    :return: the label color for this segment
    """
    if container.patches[0].get_facecolor() == (0.2549019607843137,
                                               0.25098039215686274,
                                               0.25882352941176473, 1.0):
        return 'white'
    else:
        return 'black'


def _add_segment_values(axes: plt.Axes, dataframe: pd.DataFrame, format: pd.Series) -> None:
    """
    adds segment values to the current working plot
    :param axes: the current working axes
    :param dataframe: the data sheet for the current bar plot
    :param format: the format dataframe for the current working graph
    :return:
    """
    cols = _get_data_cols(dataframe)

    for index, container in enumerate(axes.containers):
        # customize the label to account for cases when there might
        # not be a bar section
        if format['Chart Type'].lower().strip() == '100% stacked bar':
            labels = [str(round(col * 100)) + "%" for col in dataframe[cols[index]].values.tolist()]
        else:
            labels = [
                "{:,.6g}m".format(round(col / 1_000_000, DECIMAL_PLACES))
                if col >= 1_000_000 else "{:,}".format(col)
                for col in dataframe[cols[index]].values.tolist()]

        for i in range(len(labels)):
            rect = container[i]
            if _label_width(labels[i]) > rect.get_window_extent().width:
                labels[i] = ''

        plt.gca().bar_label(
            container,
            labels=labels,
            label_type='center',
            color=_get_segment_label_color(container),
            weight=FONT_WEIGHT,
            size=format['Values Font Size'])


def _add_total_values(dataframe: pd.DataFrame, format: pd.Series) -> None:
    """
    Add total values to the end of current working bars
    :param dataframe: A DataFrame that contains the data to be turned in to bars
    :param format: A pd.Series that contains the data on how the chart should be presented
    :return:
    """

    Lpercent = 0.01 * dataframe['Total'].max()
    # Add labels to each bar.
    for ypos, total in enumerate(dataframe['Total']):
        if 1_000_000 <= total <= 999_999_999:
            s = "{:,.6g}m".format(round(total / 1_000_000, DECIMAL_PLACES))
        elif total >= 1_000_000_000:
            s = "{:,.6g}bn".format(round(total / 1_000_000_000, DECIMAL_PLACES))
        elif format['Chart Type'].lower().strip() == '100% stacked bar':
            s = str(round(total * 100)) + "%"
        else:
            s = "{:,}".format(total)

        plt.text(total + Lpercent,
                 ypos,
                 s,
                 va='center',
                 weight=FONT_WEIGHT,
                 size=format['Values Font Size'])


def _add_legend(legend_labels: list[str]):
    """
    Adds a legend to the current working plot
    :param legend_labels: the labels to be used for the legend
    :return:
    """
    plt.legend(legend_labels,
               loc='lower center',
               borderaxespad=LEGEND_Y_POS,
               ncol=len(legend_labels),
               frameon=False)


def _make_bar(dataframe: pd.DataFrame, format: pd.Series, type: list[str]) -> None:
    """
    Validates the data for bar generation to ensure correct types of bars are produced
    :param dataframe: A DataFrame that contains the data to be turned in to bars
    :param format: A pd.Series that contains the data on how the chart should be presented
    :param type: a list of data headers
    :param labels: the col headers of the charts
    :return:
    """
    _generate_bars(dataframe, format, sc.get_colour_set(type))

    if format['Segment Values'].lower().strip() == 'yes':
        _add_segment_values(plt.gca(), dataframe, format)

    if format['Total Values'].lower().strip() == 'yes':
        _add_total_values(dataframe, format)

    if format['Legend'].lower().strip() == 'yes':
        # get the data column names
        _add_legend(_get_data_cols(dataframe))


def stacked_bar(dataframe: pd.DataFrame, format: pd.Series) -> plt.Figure:
    """
    Create a stacked bar plot using a given format dataframe to customize elements
    :param dataframe: a Dataframe containing the table data for this chart
    :param format: A pd.Series that contains the data on how the chart should be presented
    :return: The completed plot in the form of a module (can be used like a regular plot)
    """

    if format['Chart Size'].lower().strip() == 'full':
        ratio = 0.55
        plt.gcf().set_figwidth(CHART_WIDTH_FULL, True)
    elif format['Chart Size'].lower().strip() == 'half':
        ratio = 1.2
        plt.gcf().set_figwidth(CHART_WIDTH_HALF, True)
    plt.gcf().set_figheight(CHART_HEIGHT, True)

    _make_bar(dataframe, format, _get_data_cols(dataframe))

    if format['Gridlines/X-Axis'].lower().strip() == 'yes':
        plt.grid(visible=True, zorder=0, axis='x', color='#e6e6e6')
        if dataframe['Total'].max() != 0:
            magnitude = math.floor(math.log(dataframe['Total'].max(), 1000))
        else:
            magnitude = 0

        if 'Followers' in _get_data_cols(dataframe):
            # add grid lines to social charts
            plt.grid(visible=True, zorder=0, which='both', axis='x', color='#e6e6e6')
            # clear ticks so we can set our own
            plt.gca().set_xticklabels([])
            # create our own ticks
            plt.tick_params(axis='x', which='minor', rotation=90)
            plt.gca().xaxis.set_minor_formatter(ticker.FuncFormatter(ticker.StrMethodFormatter('{x:.0f}')))

            ax2 = plt.gca().twinx()
            ax2.annotate('', xy=(0, -0.1), xycoords='axes fraction', xytext=(1, -0.1),
                        arrowprops=dict(arrowstyle="<->", color='b'))
            ax2.spines["left"].set_position(("axes", -0.1))
            ax2.tick_params('both', length=0, width=0, which='minor')
            ax2.tick_params('both', direction='out', which='major')
            ax2.yaxis.set_ticks_position("left")
            ax2.yaxis.set_label_position("left")
            ax2.set_yticks([0.0, 0.6, 1.0])
            ax2.yaxis.set_major_formatter(ticker.NullFormatter())
            ax2.yaxis.set_minor_locator(ticker.FixedLocator([0.3, 0.8]))
            ax2.yaxis.set_minor_formatter(ticker.FixedFormatter(['mammal', 'reptiles']))

        else:
            plt.grid(visible=True, zorder=0, axis='x', color='#e6e6e6')
            plt.gca().margins(x=0,y=0)
            plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(_format_func_gen(magnitude)))

    else:
        plt.gca().set_xticklabels([])

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False)  # labels along the bottom edge are off

    plt.tick_params(axis='y', which='both', left=False, labelsize=format['Values Font Size'])

    plt.axvline(x=0, ymin=0, ymax=1, color='black', zorder=5, lw=0.5)

    plt.gca().set(xmargin=0.5)
    plt.gca().set_frame_on(False)
    # plt.gcf().set_size_inches(CHART_WIDTH_HALF,CHART_HEIGHT)

    axins = inset_axes(
        plt.gca(),
        width="5%",  # width: 50% of parent_bbox width
        height="50%",  # height: 5%
        loc="lower right",
        bbox_to_anchor=(0.07, 0, 1, 1),
        bbox_transform=plt.gca().transAxes,
        borderpad=0,
    )

    cbar = plt.gcf().colorbar(cm.ScalarMappable(
        cmap=c.ListedColormap(colors)),
        cax=axins,
        ticks=[0, 1],
        orientation='vertical'
    )
    cbar.ax.set_yticklabels(['0%', '100%'])

    x_left, x_right = plt.gca().get_xlim()
    y_low, y_high = plt.gca().get_ylim()
    plt.gca().set_aspect(abs((x_right - x_left) / (y_low - y_high)) * ratio)

    return plt.gcf()


def _add_circular_bar_labels(ax: plt.Axes, bars:container.BarContainer, angles:List[float], heights:List[float], dataframe:pd.DataFrame, lowerLimit:int) -> None:
    """
    adds labels to the end of bars for a circular bar chart
    this function should only be used for circular bar charts as it will flip labels to match the orientation of the bar
    to make it easier to read
    :param ax: the Axes of the circular bar plot
    :param bars: the BarContainer objects to have labels added to
    :param angles: the angles of each bar
    :param heights: the heights of each bar
    :param dataframe: the current working dataframe
    :param lowerLimit: the spacing of the bar from the center of the circle
    :return: None
    """
    # little space between the bar and the label
    labelPadding = 2

    # Add labels
    for bar, angle, height, label in zip(bars, angles, heights, dataframe["Name"]):

        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"

        ax.text(
            x=angle,
            y=lowerLimit + bar.get_height() + labelPadding,
            s=label,
            ha=alignment,
            va='center',
            rotation=rotation,
            rotation_mode="anchor",
            size=5)


def circular_bar(dataframe: pd.DataFrame, format: pd.Series) -> plt.Figure:
    """
    Create a circular bar plot using a given format dataframe to customize elements
    :param dataframe: a Dataframe containing the table data for this chart
    :param format: A pd.Series that contains the data on how the chart should be presented
    :return: The completed plot in the form of a module (can be used like a regular plot)
    """
    ax = plt.subplot(111, polar=True)
    plt.axis('off')

    lowerLimit = 20

    heights = dataframe.Value
    # heights = heights.replace(25, 0)

    # Compute the width of each bar.
    width = 2 * np.pi / len(dataframe.index)

    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(dataframe.index) + 1))
    angles = [element * width for element in indexes]

    # Draw bars
    bars = ax.bar(
        x=angles,
        height=heights,
        width=width,
        bottom=lowerLimit,
        color=sc.get_colour("sustainability"),
        linewidth=1,
        edgecolor="white",
    )

    _add_circular_bar_labels(ax, bars, angles, heights, dataframe, lowerLimit)

    _add_segment_values(ax, dataframe, format)

    return plt.gcf()


def _add_gradient_legend(ax:plt.Axes, legend_labels:list, colors:list):
    """
    Adds a custom legend to the current working plot
    (currently only to be used for gradient stacked plots)
    :param legend_labels: the labels to be used for the legend
    :param colors: the colors to be used for the legend
    :return:
    """

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label=legend_labels[i], markerfacecolor=colors[i], markersize=15) for
        i
        in range(len(legend_labels))
    ]

    ax.legend(handles=legend_elements, loc='upper left')


def _calculate_pos(dataframe: pd.DataFrame) -> list:
    subframe = dataframe[['Sector', "Revenue ($bn)"]]
    subframe = subframe.drop_duplicates()
    financials = list(subframe["Revenue ($bn)"])

    total_rev = sum(financials)
    sectors = list(dataframe['Sector'].unique())
    spacing = [financials[0]]
    x = [0]
    tickx = []
    for s in range(len(sectors)):
        done = False
        pos = spacing[s - 1] + (total_rev * 0.02)
        if s != 0 and not done:
            x.append(pos)
            tickx.append(pos + (financials[s] / 2))
            spacing.append(financials[s] + pos)
            done = True
        elif s == 0 and not done:
            tickx.append(financials[s] / 2)

    return x, tickx


def gradient_stacked_bar(dataframe: pd.DataFrame) -> plt.Figure:
    fig, ax = plt.subplots()
    colors = ['#FFFFFF', '#FBF3E3', '#F8E7C6', '#F4DBAA', '#F1CF8E', '#EDC371', '#EAB755', '#E6AB39', '#E39F1C', '#DF9300']
    sectors = dataframe['Sector'].unique()

    plt.gcf().set_figwidth(6.062992, True)
    plt.gcf().set_figheight(8.464567, True)

    ax.get_yaxis().set_visible(False)
    ax.xaxis.grid(False, which='minor')
    x, tickx = _calculate_pos(dataframe)
    total_largest_col = 0

    for s in range(len(sectors)):
        acc = 0
        quantile_total = 0
        for i in range(len(dataframe.index.tolist())):
            if sectors[s] == dataframe["Sector"][i]:
                if dataframe['ESG'][i] >= 0.5 and dataframe['ESG'][i] <= 1:
                    color = colors[9]
                elif dataframe['ESG'][i] >= 0.4 and dataframe['ESG'][i] <= 0.499:
                    color = colors[8]
                elif dataframe['ESG'][i] >= 0.3 and dataframe['ESG'][i] <= 0.399:
                    color = colors[7]
                elif dataframe['ESG'][i] >= 0.2 and dataframe['ESG'][i] <= 0.299:
                    color = colors[6]
                elif dataframe['ESG'][i] >= 0.15 and dataframe['ESG'][i] <= 0.199:
                    color = colors[5]
                elif dataframe['ESG'][i] >= 0.1 and dataframe['ESG'][i] <= 0.149:
                    color = colors[4]
                elif dataframe['ESG'][i] >= 0.05 and dataframe['ESG'][i] <= 0.099:
                    color = colors[3]
                elif dataframe['ESG'][i] >= 0.025 and dataframe['ESG'][i] <= 0.049:
                    color = colors[2]
                elif dataframe['ESG'][i] >= 0.01 and dataframe['ESG'][i] <= 0.025:
                    color = colors[1]
                else:
                    color = colors[0]

                bar = dataframe["Follower Quantiles"][i]
                b = ax.bar(x[s],
                            bar,
                            color=color,
                            bottom=acc,
                            edgecolor='#a09ea1',
                            linewidth=0.5,
                            align='edge',
                            width=dataframe['Revenue ($bn)'][i],
                            zorder=3)
                acc = np.add(acc, bar)
                quantile_total = quantile_total + bar
        if quantile_total > total_largest_col:
            total_largest_col = quantile_total
    pos = 0
    texts = []
    for index, container in enumerate(ax.containers):
        labels = dataframe["Brand"][index]
        bbox_points = container.patches[0].get_bbox().get_points()


        ax.annotate(text=labels,
                xy=(((bbox_points[0][0] + bbox_points[1][0]) / 2),
                    ((bbox_points[0][1] + bbox_points[1][1]) / 2)+0.1),
                fontsize=8 if (bbox_points[1][1] - bbox_points[0][1]) > 1 and total_largest_col < 100 else 4.5,
                rotation='horizontal',
                horizontalalignment='center',
                verticalalignment='center')

    ax.set_xticks(tickx, sectors)
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(True)
    ax.xaxis.grid(False, which='minor')
    ax.margins(0)
    plt.margins(0)

    # change all spines
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_color('#414042')
        ax.spines[axis].set_linewidth(0.51)

    ax.xaxis.tick_top()
    ax.xaxis.set_tick_params(which='major', top=False)
    ax.set_frame_on(False)
    ax.set_ylim(ax.get_ylim()[::-1])

    plt.gcf().set_figwidth(1.49 * 5, True)
    plt.gcf().set_figheight(1 * 5, True)

    # x_left, x_right = plt.gca().get_xlim()
    # y_low, y_high = plt.gca().get_ylim()
    # plt.gca().set_aspect(abs((x_right - x_left) / (y_low - y_high)) * 1.29)

    plt.tight_layout(pad=0, w_pad=0, h_pad=0)

    return fig


def esg_trend_bar(df:pd.DataFrame, fmt:pd.DataFrame):
    """
       Create a stacked bar plot using a given format dataframe to customize elements
       :param dataframe: a Dataframe containing the table data for this chart
       :param format: A pd.Series that contains the data on how the chart should be presented
       :return: The completed plot in the form of a module (can be used like a regular plot)
       """

    print("esg-trend: \n", df)


    fig, ax = plt.subplots()

    ty = _get_data_cols(df)
    del ty[0]

    _make_bar(df, fmt, ty)

    if fmt['Gridlines/X-Axis'].lower().strip() == 'yes':
        plt.grid(visible=True, zorder=0, axis='x', color='#e6e6e6')
        if df['Total'].max() != 0:
            magnitude = math.floor(math.log(df['Total'].max(), 1000))
        else:
            magnitude = 0
        plt.grid(visible=True, zorder=0, axis='x', color='#e6e6e6')
        ax.margins(x=0, y=0)
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(_format_func_gen(magnitude)))

    else:
        ax.set_yticklabels([])

    plt.tick_params(
        axis='y',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        top=False)  # labels along the bottom edge are off

    plt.tick_params(axis='x', which='both', left=False, bottom=False, labelsize=fmt['Values Font Size'])
    ax.set_xticks(np.arange(len(df['Quarter Start'])))
    q_ticks = _make_q_ticks(df['Quarter Start'])
    ax.set_xticklabels(q_ticks)

    dts = pd.to_datetime(df['Quarter Start'], format="%Y/%m/%d")
    years = []
    for d in dts:
        if d.year not in years:
            years.append(d.year)
    for y in range(len(years)):
        years[y] = '\n' + str(years[y])

    print("years: ", years)

    split_ticks = list(divide_chunks(ax.get_xticks(), 4))

    avgs = chunk_avg(split_ticks)
    maxis = chunk_maxi(split_ticks)
    for m in range(len(maxis)):
        maxis[m] = maxis[m] + 45

    add_class_ticks(avgs, years, plt.gca())
    add_seperator_lines(plt.gca())

    # Label bars
    min_bar_y = df['Total'].min()
    padding = (df['Total'].max() * 0.01)

    for index, row in df.iterrows():
        if row['Total'] == df['Total'].min():
            plt.gca().text(x=index, y=row['Total'] + padding, s=row['Total'], color="#F05146", ha='center')
        elif row['Total'] == df['Total'].max():
            plt.gca().text(x=index, y=row['Total'] + padding, s=row['Total'], color="#6A972D", ha='center')
        else:
            pass


    ax.set_frame_on(False)

    return plt.gcf()


def social_bar(df:pd.DataFrame, fmt:pd.DataFrame):
    fig, ax = plt.subplots()
    print("Social_Bar: ", df)

    if fmt['Chart Size'].lower().strip() == 'full':
        ratio = 0.55
        fig.set_figwidth(CHART_WIDTH_FULL, True)
    elif fmt['Chart Size'].lower().strip() == 'half':
        ratio = 1.2
        fig.set_figwidth(CHART_WIDTH_HALF, True)
    fig.set_figheight(CHART_HEIGHT, True)

    platforms = []
    max_follower = df['Followers'].max()

    for index, row in df.iterrows():
        platforms.append(row['Platform'])
        color = sc.get_colour(row['Platform'].lower()) if 'twitter' not in row['Platform'].lower() else sc.get_colour('twitter')
        bar = [row['Followers']]
        plt.barh(index,
                bar,
                color=color,
                edgecolor='none',
                height=BARWIDTH,
                zorder=3)

        if row['Followers'] < 1_000_000:
            s = "{:,.6g}k".format(round(row['Followers'] / 1_000, DECIMAL_PLACES))
        elif 1_000_000 <= row['Followers'] <= 999_999_999:
            s = "{:,.6g}m".format(round(row['Followers'] / 1_000_000, DECIMAL_PLACES))
        elif row['Followers'] >= 1_000_000_000:
            s = "{:,.6g}bn".format(round(row['Followers'] / 1_000_000_000, DECIMAL_PLACES))
        else:
            s = "{:,}".format(row['Followers'])

        if row['Followers'] == df['Followers'].max():
            acolor = '#6A972D'
        elif row['Followers'] == df['Followers'].min():
            acolor = '#F05146'
        else:
            acolor = sc.get_colour('non-sustainability')
        plt.annotate(str(s + '\n' + str(math.floor(row['Proportion'] * 100)) + '%'),
                xy=(row['Followers'] + (max_follower * 0.01), index),
                va='center',
                ha='left',
                fontsize=fmt['Values Font Size'],
                zorder=4,
                color=acolor)


    ax.set_xticklabels([])
    plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    plt.tick_params(axis='y', which='both', left=False, color=sc.get_colour('non-sustainability'))
    print(platforms)
    ax.set_yticks(range(len(platforms)))
    ax.set_yticklabels(platforms)
    plt.yticks(fontsize=12)


    # change all spines
    for axis in ['top', 'bottom', 'right']:
        plt.gca().spines[axis].set_visible(False)
    plt.gca().spines['left'].set_color('#A7A8AA')

    plt.gcf().set_size_inches(4.28, 4.79, True)

    return fig


