from pathlib import Path

import plotly.graph_objects as go
import susmon_colours
import os
from label_formatter import format_label
import pandas as pd

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


def single_layer_sankey(input_file: str):
    input_file = Path(input_file).resolve()
    df = pd.read_excel(input_file)
    df.columns = df.iloc[0]
    df = df[1:]

    for index, row in df.iterrows():
        sectors = ['Alcoholic Drinks','Beverages','Consumer Healthcare', 'Food', 'Home Care', 'Personal Care', 'Petcare', 'Tobacco', 'Other FMCG', 'Rest of business']
        sector_values = []
        sector_loc = []
        i = 0
        for s in sectors:
            sector_values.append(row[s])
            if pd.notna(row[s]):
                sector_loc.append((i, s, row[s]))
                i = i + 1
        if len(sector_loc) != 0:
            comp = (len(sector_loc), row['Company'])
            print(sector_loc)
            print(comp)
            source = []
            labels = []
            values = []
            target = [comp[0] for i in range(len(sector_loc))]
            for item in sector_loc:
                source.append(item[0])
                labels.append(item[1])
                values.append(item[2])
            print(source)
            print(target)
            print(values)
            color_list = ['#8DC63F', '#E2E41E', '#00B4AA', '#14BEF0', '#2382CA', '#965096', '#F05046', '#FDB934', '#414042', '#2382CA',
             '#14BEF0']
            colors = []
            for v in labels:
                colors.append(color_list[sectors.index(v)])
            colors.append('#FDB934')
            colors_low = []
            for c in colors:
                splitc = c.strip('#')
                rgb = tuple(int(splitc[i:i+2], 16) for i in (0, 2, 4))
                colors_low.append('rgba' + str(rgb + (0.75,)))

            print('----------')
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=labels,
                    color=colors
                ),
                link=dict(
                    source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
                    target=target,
                    value=values,
                    color = colors_low
                ))])

            fig.update_layout(font_family="Arial", title_text=comp[1] + ' Sales', font_size=12, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            fig.write_image("../../Helen/tests/" + comp[1] + ".svg")



    fig.write_html("fig1.html")


def format_labels(labels: str, length: int) -> list[str]:
    new_lbs = []
    for lb in labels:
        new_lbs.append(format_label(lb, length))
    return new_lbs


def sector_sankey(dataframe: pd.DataFrame, name: str):
    labels = dataframe['Company'].tolist()
    labels = format_labels(labels, 17)
    values = dataframe['Values'].tolist()
    for i in range(len(labels)):
        if '(estimate)' in labels[i]:
            labels[i] = f"<i><b>{labels[i].split('(')[0]}</b></i> {str(round(values[i], 1))}"
        else:
            labels[i] = f"<b>{labels[i]}</b> {str(round(values[i], 1))}"
    source = [i for i in range(len(labels))]
    target = [len(labels) for i in range(len(labels))]
    labels.insert(len(labels), f"<b>{name}</b> {round(sum(values), 1)}")

    colors = {"Alcoholic Drinks": ('rgba(240,80,70,1)', 'rgba(240,80,70,0.75)'),
              "Beverages": ('rgba(150,80,150,1)', 'rgba(150,80,150,0.75)'),
              "Consumer Healthcare": ('rgba(226,228,30,1)', 'rgba(226,228,30,0.75)'),
              "Food": ('rgba(141,198,63,1)', 'rgba(141,198,63,0.75)'),
              "Home Care": ('rgba(20,190,240,1)', 'rgba(20,190,240,0.75)'),
              "Personal Care": ('rgba(160,228,247,1)', 'rgba(160,228,247,0.75)'),
              "Pet Care": ('rgba(35,130,202,1)', 'rgba(35,130,202,0.75)'),
              "Tobacco": ('rgba(0,180,170,1)', 'rgba(0,180,170,0.75)')}
    color = colors[name]
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=color[0]
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=color[1]
        ))])

    fig.update
    fig.update_layout(font_family="Arial", title_text=name + ' Sales', font_size=12)
    fig.write_image("../../Helen/tests/" + name + ".svg")


def auto_corp_sankey(df: pd.DataFrame):
    layer1_labels = df['Layer 1 labels'].values.tolist()
    layer2_labels = df['Layer 2 labels'].values.tolist()
    layer3_labels = df['Layer 3 labels'].values.tolist()
    print(layer1_labels)
    print(layer2_labels)
    print(layer3_labels)
    layer1_values = df['Layer 1 Values'].values.tolist()
    layer2_values = df['Layer 2 Values'].values.tolist()
    layer3_values = df['Layer 3 Values'].values.tolist()

    routes = {"source": [], "dest": [], 'values': [], 'labels': []}

    snum = 0
    dnum = 0

    for i in range(len(layer1_labels)):
        if pd.notna(layer1_labels[i]):
            routes['source'].append(snum)
            routes['values'].append(layer1_values[i])
            routes['labels'].append(layer1_labels[i])
            snum = snum + 1
    for i in range(len(layer2_labels)):
        if pd.notna(layer2_labels[i]):
            routes['source'].append(snum)
            routes['values'].append(layer2_values[i])
            routes['labels'].append(layer2_labels[i])
            dnum = snum
            print(f'dnum = {dnum}')
            snum = snum + 1
            print(f'snum = {snum}')
            routes['dest'].append(dnum)
        else:
            dnum = snum - 1
            print(f'dnum = {dnum}')
            routes['dest'].append(dnum)
    for i in range(len(layer3_labels)):
        if pd.notna(layer3_labels[i]):
            routes['values'].append(layer3_values[i])
            routes['labels'].append(layer3_labels[i])
            dnum = snum + 1
            routes['dest'].append(dnum)
        # else:
        #     dnum = snum
        #     routes['dest'].append(dnum)
    print(routes)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=routes['labels'],
            color='rgba(66,135,245,1)',
        ),
        link=dict(
            source=routes['source'],
            target=routes['dest'],
            value=routes['values'],
            color='rgba(66,135,245,0.75)'
        ))])
    fig.update
    fig.update_layout(font_family="Arial", title_text='Monster Energy Sales', font_size=12)
    fig.show()


def get_layers(df:pd.DataFrame) -> list[dict]:
    '''
    get all of the layers and assign to a list of dicts
    :param df: the inpt data
    :return: list of layers with name and value
    '''
    cols = df.columns

    layer_list = []

    for i in range(0, len(cols), 2):
        labels = df[cols[i]].values.tolist()
        values = df[cols[i+1]].values.tolist()
        layer_list.append(dict(zip(labels, values)))

    print(layer_list)
    return layer_list


def get_dest(layers:list[dict], cur_layer:int, num: int) -> int:
    '''
    :param layers: list of layers dicts
    :param cur_layer: the current layer the code is on (starting from 0)
    :param num: the current source we are on
    :return: a destination index as int
    '''
    for i in range(len(layers)):
        if i != cur_layer + 1:
            for j in range(len(layers[i].keys())):
                if not pd.isna(list(layers[i].keys())[j]):
                    num = num + 1
                else:
                    num = num + 1
        else:
            return num


def get_sources(layers:list[dict]) -> list[int]:
    '''
    create a list of sources
    :param layers: a list of layer dicts
    :return:
    '''
    sources = []
    num = 0

    for i in range(len(layers) - 1):
        for j in range(len(layers[i].keys())):
            if not pd.isna(list(layers[i].keys())[j]):
                sources.append(num)
                sources.append(layers[i][list(layers[i].keys())[j]])
                num = num + 1
            else:
                num = num + 1
    return sources


def auto_sankey(df:pd.DataFrame, format:pd.DataFrame) -> go.Figure:
    '''
    generate a sankey chart from the given data
    :param df: the data for the requested sankey
    :return: the generated figure
    '''
    layers = get_layers(df)

    routes = {"source": [], "dest": [], 'values': [], 'labels': []}

    routes['source'] = get_sources()
    num = 4
    routes['dest'] = get_dest(layers, 0, num)


def main():
    print(os.getcwd())
    df = pd.read_excel("../../../Helen/Book1.xlsx", 'Sheet1')
    auto_sankey(df,df)

if __name__ == '__main__':
    main()
# single_layer_sankey("../../Helen/AUG23 - Sankey trial numbers.xlsx", "2022 Company sales by sector")
# two_layer_sankey("../../Helen/AUG23 - Sankey trial numbers.xlsx", "2022 Company sales by sector")