import matplotlib
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import pandas as pd
from datetime import timedelta
import susmon_colours as sc
import label_formatter as lbl


def check_overlap(text1, text2):
    plt.draw()
    bbox1 = text1.get_window_extent()
    bbox2 = text2.get_window_extent()

    bbox1_trans = bbox1.transformed(plt.gca().transData.inverted())
    bbox2_trans = bbox2.transformed(plt.gca().transData.inverted())

    overlap = bbox1_trans.overlaps(bbox2_trans) or bbox2_trans.overlaps(bbox1_trans)
    return overlap


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


def _get_midtime(df: pd.DataFrame, index1, index2):
    time1 = df.iloc[index1].name
    time2 = df.iloc[index2].name
    print("time1: ", time1)
    print("time2: ", time2)
    print(time1 + (time2 - time1) / 2)
    return time1 + (time2 - time1) / 2


def add_labels(last_row, corps):
    # add labels to plot lines
    x = pd.to_datetime(last_row.pop(0)) + timedelta(days=40)
    texts = []
    focal_y = 0

    for i, c in enumerate(corps):
        print('define text ' + c + ' ' + str(last_row[i]))
        current_y = last_row[i]
        if '(focal)' in c:
            lb = c.split('(focal)')[0]
            focal_y = last_row[i]
            y = focal_y
            text = plt.text(x, y, lb, fontsize=10, fontweight='bold', color='#FDB934', zorder=2)
        else:
            y = last_row[i]
            text = plt.text(x, y, c, fontsize=9, zorder=1, color='#6D6E71')

        # Check for overlaps with existing text elements
        for t in range(len(texts)):
            if current_y != last_row[t]:
                overlap = check_overlap(texts[t], text)
                if text.get_position()[1] <= focal_y:
                    padding = -0.1
                elif text.get_position()[1] > focal_y:
                    padding = 0.1
                while overlap:
                    # Handle overlapping text by adjusting the y-coordinate
                    y += padding
                    text.set_y(y)
                    overlap = check_overlap(texts[t], text)
            else:
                overlap = check_overlap(texts[t], text)
                while overlap:
                    text.set_x(text.get_position()[0] + timedelta(days=10))
                    overlap = check_overlap(texts[t], text)
        texts.append(text)


def get_center(p1, p2):
    return (p2-p1)/2

def add_class_ticks(avgs, years, ax=plt.gca(), font_size=10):
    lbs = ax.get_xticklabels()
    locs = ax.get_xticks()
    sep_locs = []

    print('locs: ', locs)
    print("lbs: ", lbs)

    p1 = 0
    p2 = 0

    for i in range(len(lbs)):
        if lbs[i].get_text() == 'Q1' or i == 0:
            p1 = locs[i]
            if i == len(lbs) - 1:
                p2 = locs[i]
                sep_locs.append(p1 + get_center(p1, p2))
            print("p1: ", p1)
        elif lbs[i].get_text() == 'Q4' or i == len(lbs) - 1:
            p2 = locs[i]
            print("p2: ", p2)
            center = p1 + get_center(p1, p2)
            print("center: ", center)
            sep_locs.append(p1 + get_center(p1, p2))

    print('sep_locs: ', sep_locs)
    print('years: ', years)
    # label the classes:
    sec = ax.secondary_xaxis(location=0)
    sec.set_xticks(sep_locs, labels=years, fontweight='bold', fontsize=font_size, color=sc.get_colour('non-sustainability'))
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


def make_ticks(dates: list):
    # Setup tick
    for d in range(len(dates)):
        if dates[d].month == 1:
            dates[d] = 'Q1'
        elif dates[d].month == 4:
            dates[d] = 'Q2'
        elif dates[d].month == 7:
            dates[d] = 'Q3'
        elif dates[d].month == 10:
            dates[d] = 'Q4'
        else:
            continue
    return dates


def get_labels_locs(df: pd.DataFrame, cols: list):
    """
    get the x and y locations for the labels
    :param df:
    :return:
    """
    high = 0
    hloc = []
    hloc_grab = True
    low = 0
    lloc = []
    lloc_grab = True
    current = 0
    for col in cols:
        if col.lower() == 'esg posts':
            high = df[col].max()
            low = df[col].min()
            print("High: ", high, "Low: ", low)
            current = df[col].iloc[-1]
            for i in range(len(df[col].tolist())):
                if df[col][i] == low and lloc_grab is True:
                    lloc.append(i)
                else:
                    if len(lloc) > 0:
                        lloc_grab = False
                if df[col][i] == high and hloc_grab is True:
                    hloc.append(i)
                else:
                    if len(hloc) > 0:
                        hloc_grab = False

    print(lloc)
    print(hloc)

    if len(lloc) == 1:
        lloc = lloc[0]
    else:
        if len(lloc) % 2 == 0:
            # Even
            lloc = lloc[len(lloc)-1] - lloc[0]
        else:
            # Odd
            lloc = lloc[len(lloc)//2]
    if len(hloc) == 1:
        hloc = hloc[0]
    else:
        hloc = hloc[-1]

    print(hloc, lloc)
    return high, low, current, hloc, lloc

def get_color(recent, low, high):
    if recent == low:
        return '#F05146'
    elif recent == high:
        return '#6A972D'
    else:
        return sc.get_colour('non-sustainability')

def time_series(df: pd.DataFrame, fmt: pd.DataFrame):
    """
    generate a time series chart from the given data
    :param df:
    :return:
    """
    dts = pd.to_datetime(df['Quarter Start'])
    dates = df['Quarter Start'].to_list()
    corps = list(df.columns.values)[1:]
    last_row = list(df.iloc[-1])
    print(last_row)
    df['Quarter Start'] = dts
    df = df.set_index('Quarter Start')
    cols = df.columns.tolist()

    high = 0
    high_index = 0
    low = 0
    low_index = 0
    recent = 0

    for col in cols:
        if '(focal)' in col:
            plt.plot(df.index, df[col], color='#FDB934', linewidth=3, zorder=2)
            high = df[col].max()
            low = df[col].min()
            recent = df[col].iloc[-1]
            for i in range(len(df[col].tolist())):
                if df[col][i] == low:
                    low_index = i
                if df[col][i] == high:
                    high_index = i
        else:
            print(df.index)
            print(df[col])
            plt.plot(df.index, df[col], color='#F4DBAA', linewidth=1, zorder=1)

    if fmt['Labels'].lower() != 'no':
        add_labels(last_row, corps)

    # Setup ticks
    for d in range(len(dates)):
        if dates[d].month == 1:
            dates[d] = 'Q1'
        elif dates[d].month == 4:
            dates[d] = 'Q2'
        elif dates[d].month == 7:
            dates[d] = 'Q3'
        elif dates[d].month == 10:
            dates[d] = 'Q4'
        else:
            continue

    years = []
    for d in dts:
        if d.year not in years:
            years.append(d.year)
    for y in range(len(years)):
        if years[y] == 'nan':
            years.pop(y)
        years[y] = '\n' + str(years[y])

    plt.gca().annotate(high, xy=(dts.iloc[high_index], high), color='green', ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    plt.gca().annotate(low, xy=(dts.iloc[low_index], low), color='red', ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    print(get_color(recent, low, high))
    plt.gca().annotate(recent, xy=(dts.iloc[-1], recent), color=get_color(recent, low, high), ha='center',
                       va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    plt.gca().plot(x_compat=True)
    plt.gca().set_xticklabels(dates, color=sc.get_colour('non-sustainability'))
    ticks = plt.gca().get_xticks()

    split_ticks = list(divide_chunks(ticks, 4))
    avgs = chunk_avg(split_ticks)
    maxis = chunk_maxi(split_ticks)
    for m in range(len(maxis)):
        maxis[m] = maxis[m] + 50

    add_class_ticks(avgs, years, plt.gca())
    add_seperator_lines(plt.gca())

    plt.yticks([])
    # change all spines
    for axis in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[axis].set_visible(False)

    plt.gca().tick_params(axis='both', which='both', length=0)

    # Set absolute sizing rather than ratio TODO: add ratio
    plt.gcf().set_figwidth(5, True)
    plt.gcf().set_figheight(5.55, True)

    return plt.gcf()


def _get_sus_ypos(sus):
    percent = (sus / 100) * 2
    return (sus / 2) - percent


def _get_total_ypos(total, max):
    return total + (max * 0.04)


def area_chart(df: pd.DataFrame, fmt: pd.DataFrame):
    """
    generate an area chart from the given data
    :param df:
    :return:
    """
    dts = pd.to_datetime(df['Quarter Start'])
    last_row = list(df.iloc[-1])
    df['Quarter Start'] = dts
    df = df.set_index('Quarter Start')
    dates = df.index.to_list()
    cols = df.columns.tolist()

    # Setup tick
    for d in range(len(dates)):
        if dates[d].month == 1:
            dates[d] = 'Q1'
        elif dates[d].month == 4:
            dates[d] = 'Q2'
        elif dates[d].month == 7:
            dates[d] = 'Q3'
        elif dates[d].month == 10:
            dates[d] = 'Q4'
        else:
            continue

    years = []
    for d in dts:
        if d.year not in years:
            years.append(d.year)
    for y in range(len(years)):
        years[y] = '\n' + str(years[y])

    plt.stackplot(df.index, df['Sustainability Posts'], df['Non-sustainability Posts'],
                  colors=[sc.get_colour('sustainability'), sc.get_colour('non-sustainability')])
    plt.plot(df.index, df['Sustainability Posts'], color='white', linewidth=3, zorder=1)

    htotal = 0
    htotalloc = 0
    htotal_midx = None
    ltotal = 0
    ltotalloc = 0
    ltotal_midx = None
    ctotal = 0
    hsus = 0
    hsusloc = 0
    hsus_midx = None
    lsus = 0
    lsusloc = 0
    lsus_midx = None
    csus = 0

    for col in cols:
        prev_y = 0
        if 'total' in col.lower():
            print(df.index)
            htotal = df[col].max()
            ltotal = df[col].min()
            ctotal = df[col].iloc[-1]
            for i in range(len(df[col].tolist())):
                if df[col][i] == ltotal:
                    if prev_y == df[col][i]:
                        ltotal_midx = _get_midtime(df, i, i - 1)
                    ltotalloc = i
                if df[col][i] == htotal:
                    if prev_y == df[col][i]:
                        htotal_midx = _get_midtime(df, i, i - 1)
                    htotalloc = i

                prev_y = df[col][i]
        if 'sus' in col.lower() and 'non' not in col.lower():
            hsus = df[col].max()
            lsus = df[col].min()
            csus = df[col].iloc[-1]
            for i in range(len(df[col].tolist())):
                if df[col][i] == lsus:
                    if prev_y == df[col][i]:
                        lsus_midx = _get_midtime(df, i, i - 1)
                    lsusloc = i
                if df[col][i] == hsus:
                    if prev_y == df[col][i]:
                        hsus_midx = _get_midtime(df, i, i - 1)
                    hsusloc = i

    # add annotations
    # Total annotaitons

    chart_max = htotal

    plt.gca().annotate(htotal,
                       xy=(htotal_midx if htotal_midx is not None else dts.iloc[htotalloc], _get_total_ypos(htotal, chart_max)),
                       color='green', ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)
    plt.gca().annotate(ltotal,
                       xy=(ltotal_midx if ltotal_midx is not None else dts.iloc[ltotalloc], _get_total_ypos(ltotal, chart_max)),
                       color='red', ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)
    plt.gca().annotate(ctotal, xy=(dts.iloc[-1], _get_total_ypos(ctotal, chart_max)), color=get_color(ctotal, ltotal, htotal),
                       ha='center',va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)

    # Sustainability annotations
    plt.gca().annotate(hsus, xy=(hsus_midx if hsus_midx is not None else dts.iloc[hsusloc], _get_sus_ypos(hsus)),
                       color='green',
                       ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)
    plt.gca().annotate(lsus, xy=(lsus_midx if lsus_midx is not None else dts.iloc[lsusloc], _get_sus_ypos(lsus)),
                       color='red',
                       ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)
    plt.gca().annotate(csus, xy=(dts.iloc[-1], _get_sus_ypos(csus)), color=get_color(csus, lsus, hsus),
                       ha='center', va='center',
                       bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'), fontsize=8.3)

    # Setup ticks
    plt.gca().set_xticklabels(dates, color=sc.get_colour('non-sustainability'), fontsize=8.3)
    ticks = plt.gca().get_xticks()

    split_ticks = list(divide_chunks(ticks, 4))
    avgs = chunk_avg(split_ticks)
    maxis = chunk_maxi(split_ticks)
    for m in range(len(maxis)):
        maxis[m] = maxis[m] + 50

    add_class_ticks(avgs, years, plt.gca(), 8.3)
    add_seperator_lines(plt.gca())

    plt.yticks([])
    # change all spines
    for axis in ['top', 'bottom', 'left', 'right']:
        plt.gca().spines[axis].set_visible(False)

    plt.gca().tick_params(axis='both', which='both', length=0)
    plt.gca().plot(x_compat=True)

    # Set absolute sizing rather than ratio TODO: add ratio
    plt.gcf().set_figwidth(5.55, True)
    plt.gcf().set_figheight(2.62, True)

    return plt.gcf()


def get_area_high(df: pd.DataFrame, cols: list):
    high = 0
    hloc = None
    for col in cols:
        if col.lower() == 'max esg posts':
            high = df[col].max()
            for i in range(len(df[col].tolist())):
                if df[col][i] == high and hloc is None:
                    hloc = i
    return high, hloc


def annotate_axis(ax, df: pd.DataFrame):
    # set up environmental
    ax.plot(df.index, df['ESG Posts'], color='#8EC63F', linewidth=3, zorder=2)
    ax.fill_between(df.index, df['Min ESG Posts'], df['Max ESG Posts'],
                     color='#8EC63F', alpha=0.25, zorder=1)
    ax.set_xticklabels(e_ticks, color=sc.get_colour('non-sustainability'))
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_visible(False)
    # line annotations
    ehigh, elow, ecurrent, ehloc, elloc = get_labels_locs(environmental, cols)
    ax.annotate(ehigh, xy=(dts.iloc[ehloc], ehigh), color='green', ha='center', va='center',
                 bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    ax.annotate(elow, xy=(dts.iloc[elloc], elow), color='red', ha='center', va='center',
                 bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    ax.annotate(ecurrent, xy=(dts.iloc[-1], ecurrent), color=sc.get_colour('non-sustainability'), ha='center',
                 va='center',
                 bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    # area annotation
    earea_high, eahloc = get_area_high(df, cols)
    cleanedList = [x for x in df['Max Corporate'].tolist() if str(x) != 'nan']
    label = ''
    for index, row in df.iterrows():
        print(row, index)
        if row['Max Corporate'] in cleanedList:
            if not row['Corporate'] != row['Max Corporate']:
                label = row['Max Corporate']
                x = index
                y = earea_high
                ax.annotate(label, xy=(x, y + 1), color=sc.get_colour('non-sustainability'),
                             ha='center',
                             va='bottom')
            else:
                x = index
                y = earea_high
                label = row['Max Corporate'] + '\n(' + str(earea_high) + ')'
                ax.annotate(label, xy=(x, y + 1), color=sc.get_colour('non-sustainability'),
                             ha='center',
                             va='bottom')

    ax1ticks = ax1.get_xticks()
    split_ticks = list(divide_chunks(ax1ticks, 4))
    ax1avgs = chunk_avg(split_ticks)
    ax1maxis = chunk_maxi(split_ticks)
    for m in range(len(ax1maxis)):
        ax1maxis[m] = ax1maxis[m] + 50

    add_class_ticks(ax1avgs, years, ax1)
    add_seperator_lines(ax1)

def get_annotation_alignment(side:str) -> str:
    if side == 'left':
        return 'right'
    elif side == 'right':
        return 'left'
    else:
        return 'center'

def esg_timeseries_section_setup(ax, df: pd.DataFrame, cols, dts, ticks, years, area_color: str, side:str):
    print("side: ", side)
    ax.plot(df.index, df['ESG Posts'], color=area_color, linewidth=3, zorder=2)
    ax.fill_between(df.index, df['Min ESG Posts'], df['Max ESG Posts'],
                     color=area_color, alpha=0.25, zorder=1)
    ax.set_xticklabels(ticks, color=sc.get_colour('non-sustainability'))
    ax.set_yticklabels([])
    ax.tick_params(axis='both', which='both', length=0)
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_visible(False)
    # line annotations
    high, low, current, hloc, lloc = get_labels_locs(df, cols)
    ax.annotate(high, xy=(dts.iloc[hloc], high), color='green', ha='center', va='center',
                 bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    ax.annotate(low, xy=(dts.iloc[lloc], low), color='red', ha='center', va='center',
                 bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))

    ax.annotate(current, xy=(dts.iloc[-1], current),
                color=sc.get_colour('non-sustainability') if current != high and current != low
                else 'red' if current == low else 'green', ha='center',
                va='center',
                bbox=dict(facecolor=(1, 1, 1, 0.75), edgecolor='white', boxstyle='round, pad=0.1'))
    # area annotation
    earea_high, eahloc = get_area_high(df, cols)
    cleanedList = [x for x in df['Max Corporate'].tolist() if str(x) != 'nan']
    label = ''
    for index, row in df.iterrows():
        if row['Max Corporate'] in cleanedList:
            if not row['Corporate'] != row['Max Corporate']:
                label = row['Max Corporate']
                x = index
                y = earea_high
                ax.annotate(label, xy=(x, y + 1), color=sc.get_colour('non-sustainability'),
                             ha=get_annotation_alignment(side),
                             va='bottom')
            else:
                x = index
                y = earea_high
                label = row['Max Corporate'] + '\n(' + str(earea_high) + ')'
                ax.annotate(label, xy=(x, y + 1), color=sc.get_colour('non-sustainability'),
                             ha=get_annotation_alignment(side),
                             va='bottom')

    ax1ticks = ax.get_xticks()
    split_ticks = list(divide_chunks(ax1ticks, 4))
    ax1avgs = chunk_avg(split_ticks)
    ax1maxis = chunk_maxi(split_ticks)
    for m in range(len(ax1maxis)):
        ax1maxis[m] = ax1maxis[m] + 50

    add_class_ticks(ax1avgs, years, ax)
    add_seperator_lines(ax)

def esg_timeseries(df: pd.DataFrame, fmt: pd.DataFrame):
    """
    generate 3 time series charts from the given data for ESG
    :param df:
    :return:
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10 * 1, 10 * 0.747), sharey=True)
    plt.subplots_adjust(wspace=0.02)
    dts = pd.to_datetime(df['Quarter Start'])
    df['Quarter Start'] = dts
    df = df.set_index('Quarter Start')
    dates = df.index.to_list()
    cols = df.columns.tolist()
    avgs = None
    maxis = None

    years = []
    for d in dts:
        if d.year not in years:
            years.append(d.year)
    for y in range(len(years)):
        years[y] = '\n' + str(years[y])

    # create groups
    grouped = df.groupby(df.Category)
    environmental = grouped.get_group("Environmental")
    e_ticks = make_ticks(list(environmental.index))
    social = grouped.get_group("Social")
    s_ticks = make_ticks(list(social.index))
    governance = grouped.get_group("Governance")
    g_ticks = make_ticks(list(governance.index))

    # set up environmental
    print("---------AX1 Environmental----------")
    esg_timeseries_section_setup(ax1, environmental, cols, dts, e_ticks, years, '#8EC63F', 'center')

    # set up social
    print("---------AX2 Social----------")
    esg_timeseries_section_setup(ax2, social, cols, dts, s_ticks, years, '#E2E41E', 'center')

    # set up governance
    print("---------AX3 Governance----------")
    esg_timeseries_section_setup(ax3, governance, cols, dts, g_ticks, years, '#00B4AB', 'center')

    return fig
