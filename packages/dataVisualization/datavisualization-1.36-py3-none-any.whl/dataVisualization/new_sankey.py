import os
from pathlib import Path

import plotly.graph_objects as go
import plotly.tools as tls
import holoviews as hv
import pandas as pd
from holoviews import opts, dim
import matplotlib.pyplot as plt
from sankeyflow import Sankey
from bokeh.io import export_svgs
hv.extension('bokeh')


def make_sankey(df:pd.DataFrame, fmt:pd.Series) -> plt.Figure:
    '''

    :param df:
    :return:
    '''
    return one_layer(df, fmt)


def get_labels(df:pd.DataFrame) -> (list[str], list[float]):
    cols = df.columns.tolist()
    label_cols = []
    value_cols = []
    for col in cols:
        if 'label' in col.lower():
            label_cols.append(col)
        elif 'value' in col.lower():
            value_cols.append(col)

    node_list = []
    for col in label_cols:
        for label in df[col].values.tolist():
            node_list.append(label)

    return list(dict.fromkeys(node_list))


def get_subsets(df:pd.DataFrame) -> list[pd.DataFrame]:
    cols = df.filter(regex="Label[0-9]+|Value[0-9]+").columns.tolist()
    col_sets = []
    x = 0
    while x < len(cols):
        col_sets.append(cols[x:x+4] + ['Monitoring'])
        x += 2

    col_sets.pop() # last index of the list will only have 2 elements so we remove it to avoid errors

    subframes = []

    for set in col_sets:
        subframes.append(df[set])

    return col_sets, subframes


def get_col_pairs(df:pd.DataFrame) -> list[pd.DataFrame]:
    cols = df.filter(regex="Label[0-9]+|Value[0-9]+").columns.tolist()
    col_sets = []
    x = 0
    while x <= len(cols):
        col_sets.append(cols[x:x+2] + ['Monitoring'])
        x += 2

    col_sets.pop() # last index of the list will only have 2 elements so we remove it to avoid errors

    subframes = []

    for set in col_sets:
        subframes.append(df[set])

    return subframes


def get_node_colors(tracked_names:dict[str, str]) -> list[str]:
    node_colors = []
    print(tracked_names)

    node_labels = list(tracked_names.keys())
    node_track = list(tracked_names.values())

    for i in range(len(node_labels)):
        print(node_labels[i])
        print(node_track[i])

        if node_track[i].lower() == 'yes':
            if 'change' in node_labels[i].lower():
                node_colors.append('rgba(141, 198, 63, 1)')
            elif 'other[' in node_labels[i].lower():
                node_colors.append('rgba(65, 64, 66, 1)')
            elif 'susmon_' in node_labels[i]:
                node_colors.append('rgba(253,185,52,1)')
            elif 'skip' in node_labels[i].lower():
                node_colors.append('rgba(35, 130, 202, 0.5)')
            else:
                node_colors.append('rgba(35, 130, 202, 1)')
        else:
            node_colors.append('rgba(65, 64, 66, 1)')

    return node_colors


def get_link_colors(stv:list[tuple], node_labels:list[str]) -> list[str]:
    link_colors = []

    for link in stv:
        node_name = node_labels[link[1]]
        if 'susmon_' in node_name:
            if link[3].lower() == 'yes':
                link_colors.append('rgba(253,185,52,0.5)')
            else:
                link_colors.append('rgba(65, 64, 66, 0.5)')
        elif 'other[' in node_name.lower():
            link_colors.append('rgba(65, 64, 66, 0.5)')
        else:
            link_colors.append('rgba(35, 130, 202, 0.5)')

    return link_colors


def adjust_labels(node_labels:list[str], values:list[float], est:list[bool]) -> list[str]:
    '''

    :param node_labels:
    :return:
    '''
    new_labels = []
    new_values = []

    for v in values:
        new_values.append(round(v, 1))
    print(new_values)

    for lb in range(len(node_labels)):
        if est[lb]:
            value = '~' + str(new_values[lb])
        else:
            value = str(new_values[lb])

        if '[' in node_labels[lb]:
            label = node_labels[lb].split('[')[0] + ' (' + value + ')'
        elif 'change' in node_labels[lb] or 'Not' in node_labels[lb] or 'skip' in node_labels[lb]:
            label = ''
        else:
            label = node_labels[lb] + ' (' + value + ')'

        if 'susmon_' in node_labels[lb]:
            label = label.split('susmon_')[1]

        new_labels.append(label)

    return new_labels


def get_tracking(df:pd.DataFrame, node_labels:list[str]):
    '''
    create dict of node names and if they are tracked or not
    :param df:
    :return:
    '''

    names_tracking = {}

    monitoring_loc = df.columns.get_loc('Monitoring')
    monitoring_slice = df.iloc[:,[monitoring_loc-3, monitoring_loc-2, monitoring_loc]]

    for node in node_labels:
        names_tracking[node] = 'yes'

    for index, row in monitoring_slice.iterrows():
        print(row)
        if row[0] in names_tracking and 'no' in row[2].lower():
            names_tracking[row[0]] = row[2]

    return names_tracking


def get_values(subframes:list[pd.DataFrame]):
    '''
    take  list of subframes and retunr a dict of node_label and node_value
    :param subframes:
    :return:
    '''

    label_value_pair = {}
    estimates = {}


    for frame in subframes:
        for index, row in frame.iterrows():
            name = row.iloc[0]
            estimate = False

            if '~' in str(row.iloc[1]):
                value = float(row.iloc[1].split('~')[1])
                estimate = True
            else:
                value = row.iloc[1]

            estimates[name] = estimate

            if name in label_value_pair.keys():
                label_value_pair[name] = label_value_pair[name] + value
            else:
                label_value_pair[name] = value

    return list(label_value_pair.values()), list(estimates.values())


def one_layer(df:pd.DataFrame, fmt:pd.DataFrame) -> plt.Figure:
    '''
    produce single layer sankey chart
    :param df:
    :return:
    '''

    node_labels = get_labels(df)
    node_id = list(range(len(node_labels)))

    stv = []  # stv stands for source, target, value, monitoring. It holds a list of all of the connections

    tracked_names = get_tracking(df, node_labels)

    # Get a list of colors for the Node elements
    node_colors = get_node_colors(tracked_names)

    # Create subsets of the dataframe so we can iterate 4 cols at a time
    col_sets, subframes = get_subsets(df)


    # Loop through subsets to fill stv with the paths
    for set in range(len(subframes)):
        for index, row in subframes[set].iterrows():

            source = node_labels.index(row[col_sets[set][0]])
            target = node_labels.index(row[col_sets[set][2]])
            if type(row[col_sets[set][3]]) == str:
                value = float(row[col_sets[set][3]].split('~')[1])
            else:
                value = row[col_sets[set][3]]
            monitor = row[col_sets[set][4]]
            stv.append((source, target, value, monitor))



    # Generate a list of colors for the links between nodes
    link_colors = get_link_colors(stv, node_labels)


    values, estimates = get_values(get_col_pairs(df))
    print(values)

    if 'yes' in fmt['Labels'].lower():
        # Fix node labels
        node_labels = adjust_labels(node_labels, values, estimates)
    else:
        node_labels = []


    source, target, values, monitor = zip(*stv)

    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=15,
            thickness=20,
            x=[0],
            y=[0],
            label=node_labels,
            line=dict(width=0),
            color=node_colors,

        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=link_colors
        ))],
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        ))

    fig.update_traces(
        textfont_size=8,
        selector=dict(type='sankey'))

    fig.update_layout(
        font_color='rgb(65, 64, 66)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=(476),  # Set the height of the figure to 600 pixels
        width=(833)  # Set the width of the figure to 800 pixels
    )

    return fig

