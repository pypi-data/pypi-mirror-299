"""
This is the script for the dataVisualization function where Excel files are read and converted to dataframes,
these dataframes are then manipulated to be sent to pies.py and bars.py to be converted to plots
with matplotlib and finally saved as png images
"""

import argparse
import matplotlib
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import os
import logging
from pathlib import Path

import dataVisualization.bars as susmon_bars
import dataVisualization.pies as susmon_pies
import dataVisualization.treemap as susmon_treemap
import dataVisualization.new_sankey as susmon_sankey
import dataVisualization.time_series as susmon_time
import dataVisualization.susmon_colours as sc
from dataVisualization.exceptions import MissingFormatSheetError, InvalidFormatSheetError, InvalidInputDataError


RESOLUTION = 600
SAVE_TYPE = '.svg'

# use matplotlib is agg form (an exclusivly backend form that does not attempt to open a gui prompt)
plt.close('all')
matplotlib.use('agg')

# specify the custom font to use
plt.rcParams['font.family'] = 'Arial'


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# configure some basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(__name__+".log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def _save_file(figure: plt.Figure, save_loc: Path) -> None:
    """
    Takes a given plot and saves it to a file
    :param figure:
    :param save_loc:
    :return:
    """
    if type(figure) == go.Figure:
        print(save_loc)
        figure.write_image(file=save_loc)
        html_path = os.path.splitext(str(save_loc))[0] + '.html'
        print(html_path)
        figure.write_html(html_path)

        # make sure html is saving as svg rather than the defualt of png
        with open(html_path, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace('png', 'svg')

        # Write the file out again
        with open(html_path, 'w') as file:
            file.write(filedata)

        figure.data = []
    else:
        figure.savefig(save_loc, bbox_inches='tight', dpi=RESOLUTION, pad_inches=0)
    plt.close('all')


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(description='Generate SusMon charts')
    parser.add_argument('input_dir',
                        help='input directory containing .xlsx files')
    parser.add_argument('--ignore-bars',
                        help='skip generation of bar charts',
                        action='store_true')
    parser.add_argument('--ignore-pies',
                        help='skip generation of pie charts',
                        action='store_true')

    return parser.parse_args()


def main_cmd(args: argparse.Namespace):
    """
    This is the dataVisualization loop for the software that performs a few things.
    1. it loops through all of the Excel files in the given directory
    2. open the Excel file as a dataframe
    3. work out which charts are for pies and which are for bars (using getgraphs function)
    4. loop through the sheets and generate the correct charts for the given sheet (bar/graph)
    5. save this file in a given directory
    :return:
    """
    input_path = Path(args.input_dir).resolve()

    for file in input_path.iterdir():
        print(file)
        # ignore non-.xlsx and temporary files
        if file.suffix != '.xlsx' or '~$' in file.stem:
            continue

        # create unique output directory <file>_charts/
        output_path = file.with_name(file.stem + '_charts')
        if not output_path.is_dir():
            output_path.mkdir()

        datasheets: dict[str, pd.DataFrame] = pd.read_excel(file, sheet_name=None)
        names = list(datasheets.keys())
        dfs = list(datasheets.values())

        # ensure format sheet is present
        try:
            format = datasheets['Format'].set_index('Sheet No.')
        except KeyError:
            raise MissingFormatSheetError('All')

        # missing 'Slide No.' column will cause set_index to return None
        if format is None:
            raise InvalidFormatSheetError

        format.index = format.index.map(str)

        xls = pd.ExcelFile(file)
        sheets = xls.book.worksheets

        for i in range(len(dfs)):
            print(names[i])
            if sheets[i].sheet_state != 'visible':
                continue
            if names[i] in ['Instructions', 'Formula', 'Parameters', 'Format', 'Version Control', 'Version Ctrl','Brief', 'Problem Corps']:
                continue
            elif names[i] in format.index.tolist():
                if not args.ignore_bars:
                    fr = format.loc[names[i]]
                    if fr['Chart Type'].lower == "ignore":
                        logger.debug("sheet is not chart data: " + names[i])
                        continue
                    elif fr['Chart Type'].lower().strip() == "circular bar":
                        plot = susmon_bars.circular_bar(dfs[i], fr)
                    elif fr['Chart Type'].lower() == "gradient stackbars" or fr['Chart Type'].lower() == "marimekko":
                        plot = susmon_bars.gradient_stacked_bar(dfs[i])
                    elif fr['Chart Type'].lower() == 'esg trend bar':
                        plot = susmon_bars.esg_trend_bar(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'treemap':
                        plot = susmon_treemap.make_treemap(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'time series' or fr['Chart Type'].lower() == 'line':
                        plot = susmon_time.time_series(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'area':
                        plot = susmon_time.area_chart(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'area/line':
                        plot = susmon_time.esg_timeseries(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'social bar':
                        plot = susmon_bars.social_bar(dfs[i], fr)
                    elif 'sankey' in fr['Chart Type'].lower():
                        print(fr['Chart Type'])
                        plot = susmon_sankey.make_sankey(dfs[i], fr)
                    else:
                        plot = susmon_bars.stacked_bar(dfs[i], fr)

                    if "Category" in dfs[i]:
                        _save_file(plot, output_path / (names[i] + " - " + dfs[i]["Category"][0] + SAVE_TYPE))
                    else:
                        _save_file(plot, output_path / (names[i] + SAVE_TYPE))
            else:
                if not args.ignore_pies:
                    try:
                        plot = susmon_pies.doughnut(dfs[i])
                        _save_file(plot, output_path / (names[i] + " - " + str(dfs[i].iloc[0,0]) + SAVE_TYPE))
                    except InvalidInputDataError as e:
                        print(InvalidInputDataError(names[i]))


def main(file: str, output_path: Path, ignore_bars=False, ignore_pies=False):
    """
    This is the dataVisualization loop for the software that performs a few things.
    1. it loops through all of the Excel files in the given directory
    2. open the Excel file as a dataframe
    3. work out which charts are for pies and which are for bars (using getgraphs function)
    4. loop through the sheets and generate the correct charts for the given sheet (bar/graph)
    5. save this file in a given directory
    :return:
    """
    input_file = Path(file).resolve()

    logger.debug("API Version using file: " + str(input_file))
    # ignore non-.xlsx and temporary files
    
    if input_file.suffix == '.xlsx' and not '~$' in input_file.stem:

        # create unique output directory <file>_charts/
        logger.debug("About to make directory: " + str(output_path))

        if not output_path.is_dir():
            os.makedirs(output_path)

        datasheets: dict[str, pd.DataFrame] = pd.read_excel(input_file, sheet_name=None)
        names = list(datasheets.keys())
        dfs = list(datasheets.values())

        # ensure format sheet is present
        try:
            format = datasheets['Format'].set_index('Sheet No.')
        except KeyError:
            raise MissingFormatSheetError('All')

        # missing 'Slide No.' column will cause set_index to return None
        if format is None:
            raise InvalidFormatSheetError

        format.index = format.index.map(str)

        xls = pd.ExcelFile(file)
        sheets = xls.book.worksheets

        for i in range(len(dfs)):
            logger.debug("working on sheet: " + names[i])
            if sheets[i].sheet_state != 'visible':
                logger.debug("sheet is not visible: " + names[i])
                continue
            if names[i] in ['Instructions', 'Formula', 'Parameters', 'Format', 'Version Control']:
                logger.debug("sheet is not chart data: " + names[i])
                continue
            elif names[i] in format.index.tolist():
                logger.debug("sheet is in our format table as: " + names[i])
                if not ignore_bars:
                    logger.debug("we are not ignoring bars")
                    fr = format.loc[names[i]]
                    if fr['Chart Type'].lower == "ignore":
                        logger.debug("sheet is not chart data: " + names[i])
                        continue
                    elif fr['Chart Type'].lower() == "circular bar":
                        logger.debug("plotting circular bar")
                        plot = susmon_bars.circular_bar(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'treemap':
                        logger.debug("plotting treemap")
                        plot = susmon_treemap.make_treemap(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'marimekko':
                        plot = susmon_bars.gradient_stacked_bar(dfs[i])
                    elif fr['Chart Type'].lower() == 'time series':
                        plot = susmon_time.time_series(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'area':
                        plot = susmon_time.area_chart(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'area/line':
                        plot = susmon_time.esg_timeseries(dfs[i], fr)
                    elif fr['Chart Type'].lower() == 'social bar' or fr['Chart Type'].lower() == 'esg trend bar':
                        plot = susmon_bars.social_bar(dfs[i], fr)
                    else:
                        logger.debug("plotting stacked bar")
                        plot = susmon_bars.stacked_bar(dfs[i], fr)

                    if "Category" in dfs[i]:
                        logger.debug("saving with category: " + dfs[i]["Category"][0] + " to: " + (names[i] + " - " + dfs[i]["Category"][0] + SAVE_TYPE))
                        _save_file(plot, output_path / (names[i] + " - " + dfs[i]["Category"][0] + SAVE_TYPE))
                    else:
                        logger.debug("saving without a category to: " + (names[i] + SAVE_TYPE))
                        _save_file(plot, output_path / (names[i] + SAVE_TYPE))
                else:
                    logger.debug("we are ignoring bars")
            else:
                if not ignore_pies:
                    try:
                        logger.debug("plotting pie")
                        plot = susmon_pies.doughnut(dfs[i])
                        _save_file(plot, output_path / (names[i] + " - " + str(dfs[i].iloc[0,0]) + SAVE_TYPE))
                    except InvalidInputDataError as e:
                        print(InvalidInputDataError(names[i]))
                        
    return str(output_path)



if __name__ == '__main__':
    plt.close('all')
    _args = _parse_args()
    main_cmd(_args)

