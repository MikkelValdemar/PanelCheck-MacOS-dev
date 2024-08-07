from PlotData import CollectionCalcPlotData, MM_ANOVA_PlotData
from Progress_Info import Progress
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator
from matplotlib.colors import LinearSegmentedColormap

import wx
import os
import sys
import numpy as np

# custom colormap
colormaps = {}
color_dict = {'red': ((0.0, 0.0, 0.0),
                      (0.5, 0.5, 0.5),
                      (1.0, 1.0, 1.0)),
              'green': ((0.0, 0.0, 0.0),
                        (0.5, 0.5, 0.5),
                        (1.0, 1.0, 1.0)),
              'blue': ((0.0, 0.0, 0.0),
                       (0.5, 0.5, 0.5),
                       (1.0, 1.0, 1.0))}

color_dict_green = {'red': ((0.0, 0.0, 0.0),
                            (0.5, 0.0, 0.0),
                            (1.0, 0.0, 0.0)),
                    'green': ((0.0, 0.0, 0.0),
                              (0.5, 0.5, 0.5),
                              (1.0, 1.0, 1.0)),
                    'blue': ((0.0, 0.0, 0.0),
                             (0.5, 0.0, 0.0),
                             (1.0, 0.0, 0.0))}

# manhattan night
color_dict2 = {'red': ((0.0, 0.0, 0.0),
                       (0.7, 0.0, 1.0),
                       (1.0, 1.0, 1.0)),
               'green': ((0.0, 0.0, 0.0),
                         (0.7, 0.0, 0.7),
                         (1.0, 1.0, 1.0)),
               'blue': ((0.0, 0.0, 0.0),
                        (0.7, 1.0, 0.0),
                        (1.0, 1.0, 1.0))}

# manhattan sunset
color_dict3 = {'red': ((0.0, 0.8, 0.8),
                       (0.7, 1.0, 0.0),
                       (1.0, 0.3, 0.3)),
               'green': ((0.0, 0.0, 0.0),
                         (0.7, 0.7, 0.0),
                         (1.0, 0.3, 0.3)),
               'blue': ((0.0, 0.0, 0.0),
                        (0.7, 0.0, 0.0),
                        (1.0, 0.3, 0.3))}

# Manhattan Colormap
colormaps['manhattan'] = LinearSegmentedColormap('manhattan', color_dict, 256)

# 14 colors:
colors_hex_list = [
    '#FF0000',
    '#00F600',
    '#1111FF',
    '#FFCC00',
    '#CF00F6',
    '#00F6CF',
    '#444444',
    '#999999',
    '#f27200',
    '#016f28',
    '#840084',
    '#0082a2']

# 14 colors:
colors_rgb_list = [
    (1,
     0,
     0),
    (0,
     0.866667,
     0),
    (0,
     0,
     1),
    (1,
     0.8,
     0),
    (0.8,
     0,
     0.933333),
    (0,
     0.933333,
     0.733333),
    (0.4,
     0.4,
     0.4),
    (0.8,
     0.8,
     0.8),
    (0.666667,
     0.4,
     0.4),
    (0.4,
     0.666667,
     0.4),
    (0.4,
     0.4,
     0.666667),
    (0.666667,
     0.6,
     0.4),
    (0.666667,
     0.4,
     0.6),
    (0.4,
     0.666667,
     0.6)]


def assign_colors(assessorList, replicateList):
    """
    Returns color dictionary
    Assigns same color for each assessor (for both active and non-active assessors).

    keys: (Assessor, Replicate)
    value: [color, shape]
    """

    # Symbols list, used in all plots
    all_colors = [
        '#FF0000',
        '#00F600',
        '#1111FF',
        '#FFCC00',
        '#CF00F6',
        '#00F6CF',
        '#444444',
        '#999999',
        '#f27200',
        '#016f28',
        '#840084',
        '#0082a2']
    # all_colors = [(0.75,0.0,0.0), (1.0,0.33,0.33), (0.66,0.66,0.0), (1.0,0.5,0.0), (0.33,0.75,0.0), (0.33,1.0,0.33), (0.33,0.66,0.66), (0.0,0.9,0.9), (0.33,0.5,0.75), (0.5,0.33,1.0), (0.66,0.0,0.66), (0.9,0.0,0.75)]
    """
          b  : blue
          g  : green
          r  : red
          c  : cyan
          m  : magenta
          y  : yellow
          k  : black
          w  : white
    """
    # all_colors = []
    # for r in range(0,10):
    #    for g in range(0, 10):
    #        for b in range(0, 10):
    #             color = (r*0.1, g*0.1, b*0.1)
    #             all_colors.append([color])
    shapes = ['o', 'd', 's', '^', '>', 'v', '<', 'p', 'h', '8']
    """
        's' : square
        'o' : circle
        '^' : triangle up
        '>' : triangle right
        'v' : triangle down
        '<' : triangle left
        'd' : diamond
        'p' : pentagram
        'h' : hexagon
        '8' : octagon
    """

    index = 0
    i_max = len(all_colors)
    rep_max = len(shapes)

    colors = {}

    for ass in assessorList:
        rep_index = 0
        for rep in replicateList:
            colors[(ass, rep)] = [all_colors[index], shapes[rep_index]]
            rep_index += 1
            if rep_index >= rep_max:
                rep_index = 0
        index += 1
        if index >= i_max:
            index = 0

    return colors


def set_xlabeling(ax, x_string_list, font_size=13, x_positions=None):
    """
    Sets x-labels by given x_string_list onto ax
    """
    font = {'fontname': 'Arial Narrow',
            'color': 'black',
            'fontweight': 'normal',
            'fontsize': font_size}

    amount = len(x_string_list)

    if x_positions is None or (len(x_positions) != len(x_string_list)):
        # arangement of lables for step=1.0

        x_range = ax.get_xlim()
        start_x = (x_range[1] - (amount)) / 2
        part = ((x_range[1] - 2 * start_x) / amount)
        spacer = part / 2

        x_positions = []
        for i in range(0, amount):
            x_positions.append(start_x + spacer + i * part)

    # print tickPositions
    locator = FixedLocator(x_positions)
    ax.xaxis.set_major_locator(locator)
    ax.set_xticklabels(x_string_list, fontdict=font)


def set_ylabeling(ax, y_string_list, font_size=13):
    """
    Sets x-labels by given x_string_list onto ax
    """
    font = {'fontname': 'Arial Narrow',
            'color': 'black',
            'fontweight': 'normal',
            'fontsize': font_size}

    amount = len(y_string_list)
    y_range = ax.get_ylim()
    start_y = (y_range[1] - amount) / 2
    part = ((y_range[1] - 2 * start_y) / amount)
    spacer = part / 2

    y_positions = []
    for i in range(0, amount):
        y_positions.append(start_y + spacer + i * part)

    # print tickPositions
    locator = FixedLocator(y_positions)
    ax.yaxis.set_major_locator(locator)
    ax.set_yticklabels(y_string_list, fontdict=font)


def set_xlabeling_rotation(ax, rotation, fontsize=10):
    """
    rotation: 'horizontal', 'vertical' or angle
    """
    fig = ax.figure
    bboxes = []
    for xtick_label in ax.get_xticklabels():
        xtick_label._rotation = rotation
        # bbox = xtick_label.get_window_extent()
        # the figure transform goes from relative coords->pixels and we
        # want the inverse of that
        # bboxi = bbox.inverse_transformed(fig.transFigure)
        # bboxes.append(bboxi)

    # this is the bbox that bounds all the bboxes, again in relative
    # figure coords
    # bbox = Bbox.union(bboxes)
    # if fig.subplotpars.bottom < bbox.height:
    # we need to move it over
    # fig.subplots_adjust(bottom=1.1*bbox.height) # pad a little

    # xtick_label._fontproperties.set_size(fontsize)

    # cut label:
    # print xtick_label.get_text()
    # if num_of_chars > 0 and num_of_chars < len(xtick_label._text):
    #    xtick_label.set_text(xtick_label.get_text()[0:num_of_chars] + "..")
    #    print xtick_label.get_text()


def set_axis_labelsize(ax, fontsize):
    for text_element in ax.get_xticklabels():
        text_element._fontproperties.set_size(fontsize)
    for text_element in ax.get_yticklabels():
        text_element._fontproperties.set_size(fontsize)


def axes_create(legend, fig, aspect='auto'):
    """
    Creates figure axes.

    @type legend: boolean
    @param legend: Whether legend is on or off.
    """
    ax = 0
    if (legend):  # if legend to be drawn
        # [left, bottom, width, height]
        ax = fig.add_axes([0.1, 0.1, 0.65, 0.8], aspect=aspect)
    else:
        # [left, bottom, width, height]
        ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], aspect=aspect)
    return ax


def axes_setup(ax, xLabel, yLabel, title, limits, font_size=13):
    """
    Sets up the axes.

    @type ax: object
    @param ax: Axes to be worked on.

    @type title: string
    @param title: Axes title.

    @type xLabel: string
    @param xLabel: Label name under the x-axes.

    @type yLabel: string
    @param yLabel: Label name left of the y-axes.

    @type limits: list
    @param limits: Limits for the axes. [x_min, x_max, y_min, y_max]
    """
    font = {'fontname': 'Arial Narrow',
            'color': 'black',
            'fontweight': 'normal',
            'fontsize': font_size}

    # Settings for the labels in the plot
    ax.set_xlabel(xLabel, font)
    ax.set_ylabel(yLabel, font)
    ax.set_title(title, font)

    if np.isscalar(limits[0]):
        ax.set_xlim(limits[0], limits[1])
        ax.set_ylim(limits[2], limits[3])
    else:
        ax.set_xlim(limits[0].item(), limits[1].item())
        ax.set_ylim(limits[2].item(), limits[3].item())


def check_point(x, y, epsilon, pointAndLabelList, max):
    """
    If a plotting point is at the exact same point as another, it will be
    moved -epsilon on the x-axis. Returns the new x value.
    """
    for point in pointAndLabelList:
        if point[0] == x and point[1] == y:
            if point[3] < max:
                x = x - epsilon * point[3]
                point[3] += 1
                return x
    return x


def equal_lists(listA, listB):
    # import pdb
    # pdb.set_trace()
    a = len(listA)
    b = len(listB)
    if a != b:
        return False

    for i in range(a):
        if listA[i] != listB[i]:
            return False
    return True


def show_err_msg(msg):
    dlg = wx.MessageDialog(None, msg, 'Error Message',
                           wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


def show_info_msg(msg):
    dlg = wx.MessageDialog(None, msg, 'Important Information',
                           wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


def show_msg(msg, title):
    dlg = wx.MessageDialog(None, msg, title,
                           wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy()


############### general raw data ###############
def raw_data_grid(
        s_data,
        plot_data,
        active_assessors=None,
        active_attributes=None,
        active_samples=None,
        active_replicates=None):
    """
    Returns string array of raw data. For use in Grid.
    Raw data based on the active lists.
    """
    rawDataList = []
    emptyLine = ['']
    headerRawData = ['Raw Data']
    underline = ['========']

    if active_assessors is None:
        active_assessors = plot_data.activeAssessorsList
    if active_attributes is None:
        active_attributes = plot_data.activeAttributesList
    if active_samples is None:
        active_samples = plot_data.activeSamplesList
    if active_replicates is None:
        active_replicates = s_data.ReplicateList

    att_indices = []
    for att in active_attributes:
        # the same order as in self.SparseMatrix:
        att_indices.append(s_data.AttributeList.index(att))

    if s_data.has_mv:
        print("has missing values")
        line_ind = 0
        missing_pos = []
        rawDataList.append(headerRawData)
        rawDataList.append(underline)
        rawDataList.append(emptyLine)
        line_ind += 4

        attributeLine = ['Assessor', 'Sample', 'Replicate']
        attributeLine.extend(plot_data.activeAttributesList)
        rawDataList.append(attributeLine)

        for assessor in active_assessors:

            for sample in active_samples:

                for replicate in active_replicates:

                    attributeValues = []
                    for att_ind in att_indices:
                        singleAttributeValue = s_data.SparseMatrix[(
                            assessor, sample, replicate)][att_ind]
                        attributeValues.append(singleAttributeValue)

                    col_ind = 0
                    if (assessor, sample, replicate) in s_data.mv_pos:
                        for att_ind in att_indices:
                            if att_ind in s_data.mv_pos[(
                                    assessor, sample, replicate)]:
                                missing_pos.append((line_ind, col_ind + 3))
                            col_ind += 1

                    dataLine = [assessor, sample, replicate]
                    dataLine.extend(attributeValues)
                    rawDataList.append(dataLine)
                    line_ind += 1
        plot_data.raw_data_mv_pos = missing_pos
        return rawDataList
    else:

        rawDataList.append(headerRawData)
        rawDataList.append(underline)
        rawDataList.append(emptyLine)

        attributeLine = ['Assessor', 'Sample', 'Replicate']
        attributeLine.extend(plot_data.activeAttributesList)
        rawDataList.append(attributeLine)

        for assessor in active_assessors:

            for sample in plot_data.activeSamplesList:

                for replicate in s_data.ReplicateList:

                    attributeValues = []
                    for attribute in plot_data.activeAttributesList:
                        singleAttributeValue = s_data.SparseMatrix[(
                            assessor, sample, replicate)][s_data.AttributeList.index(attribute)]
                        attributeValues.append(singleAttributeValue)

                    dataLine = [assessor, sample, replicate]
                    dataLine.extend(attributeValues)
                    rawDataList.append(dataLine)
        return rawDataList


############### numerical data for ANOVA ###############
def numerical_data_grid(
        s_data,
        plot_data,
        ANOVA_F,
        ANOVA_p,
        ANOVA_MSE,
        F_significances):
    import pdb
    """
    Return list of numerical data
    """
    resultList = []
    emptyLine = ['']
    numericResultsHeader = ['ANOVA (one-way) results']
    underline = ['================']
    resultList.append(numericResultsHeader)
    resultList.append(underline)
    resultList.append(emptyLine)
    resultList.append(['F @ 1% significance level:', str(F_significances[0])])
    resultList.append(['F @ 5% significance level:', str(F_significances[1])])
    resultList.append(emptyLine)

    for ass_ind in range(len(plot_data.activeAssessorsList)):
        assessorLine = [plot_data.activeAssessorsList[ass_ind], '', '', '', '']
        headerLine = ['Nr.', 'Attribute', 'F value', 'p value', 'MSE value']
        resultList.append(assessorLine)
        resultList.append(headerLine)

        for att_ind in range(len(plot_data.activeAttributesList)):
            actual_att_ind = s_data.AttributeList.index(
                plot_data.activeAttributesList[att_ind])
            # Constructing the line that contains calculation-results
            print(att_ind)
            valueLine = [
                actual_att_ind + 1,
                plot_data.activeAttributesList[att_ind],
                num2str(
                    ANOVA_F[ass_ind][att_ind],
                    fmt="%.2f"),
                num2str(
                    ANOVA_p[ass_ind][att_ind]),
                num2str(
                    ANOVA_MSE[ass_ind][att_ind],
                    fmt="%.2f")]
            resultList.append(valueLine)
        resultList.append(emptyLine)

    return resultList


############### numerical data part PCA scores ###############
def numerical_data_add_scores(
        scores_array,
        object_names,
        maxPCs,
        numeric_data=[],
        header_txt='PCA scores:'):
    headerLine = [header_txt]
    numeric_data.append(headerLine)

    (rows, cols) = scores_array.shape

    matrixHeaderLine = ['']
    for PC in range(maxPCs):
        matrixHeaderLine.append('PC ' + str(PC + 1))
    numeric_data.append(matrixHeaderLine)

    for obj_ind in range(rows):
        scoresRow = [object_names[obj_ind]]
        scores = []
        for PC in range(maxPCs):
            scores.append(num2str(scores_array[obj_ind, PC]))
        scoresRow.extend(scores)
        numeric_data.append(scoresRow)

    return numeric_data


############### numerical data part PCA loadings ###############


def numerical_data_add_loadings(
        loadings_array,
        variable_names,
        maxPCs,
        numeric_data=[],
        header_txt='PCA loadings:'):
    headerLine = [header_txt]
    numeric_data.append(headerLine)

    matrixHeaderLine = ['']
    matrixHeaderLine.extend(variable_names)
    numeric_data.append(matrixHeaderLine)

    (rows, cols) = loadings_array.shape

    for PC in range(maxPCs):
        loadingsRow = ['PC ' + str(PC + 1)]
        loadings = []
        for var_ind in range(cols):
            loadings.append(num2str(loadings_array[PC, var_ind]))
        loadingsRow.extend(loadings)
        numeric_data.append(loadingsRow)

    return numeric_data


############### numerical data np.single row ###############
def str_row(a, fmt="%.2f"):
    _list = []
    for x in a:
        _list.append(num2str(x, fmt=fmt))
    return _list


def num2str(x, fmt='%.3f'):
    if isinstance(x, (float, int)):
        return fmt % (x)
    else:
        return x


############### general test methods ###############

def check_columns(X):
    """
    Check that columns vectors do not have STD=0. For STD=0 the column/attribute vector must be removed
    for current analysis.
    """

    (rows, cols) = np.shape(X)
    out_cols = []
    in_cols = []

    for col_ind in range(cols):
        # print std(X[:, col_ind])

        if np.std(X[:, col_ind]) == 0:
            out_cols.append(col_ind)
        else:
            in_cols.append(col_ind)

    if len(out_cols) == 0:
        return X, []
    else:
        new_X = np.zeros((rows, len(in_cols)), float)
        new_col_ind = 0
        for col_ind in in_cols:
            new_X[:, new_col_ind] = X[:, col_ind]
            new_col_ind += 1

        return new_X, out_cols


def attribute_significance(s_data, plot_data, one_rep=False, abspath=None):
    from MM_ANOVA_Plot import load_mm_anova_data
    activeAssessorsList = plot_data.activeAssessorsList
    activeAttributesList = plot_data.activeAttributesList
    activeSamplesList = plot_data.activeSamplesList
    new_active_attributes_list = activeAttributesList

    matrix_selected_scores = s_data.MatrixDataSelected(
        assessors=activeAssessorsList,
        attributes=activeAttributesList,
        samples=activeSamplesList)

    matrix_selected_scores, out_cols = check_columns(matrix_selected_scores)
    if len(out_cols) > 0:
        msg = "For the selected samples the standard deviation\nover all assessors is 0 for the following attributes:\n"
        for col_ind in out_cols:
            msg += plot_data.activeAttributesList[col_ind] + "\n"

        msg += "\nThese attributes were left out of the analysis."

        new_active_attributes_indices = []
        new_active_attributes_list = []
        for att_ind in range(len(plot_data.activeAttributesList)):
            if att_ind not in out_cols:
                new_active_attributes_indices.append(att_ind)

        for att_ind in new_active_attributes_indices:
            new_active_attributes_list.append(
                plot_data.activeAttributesList[att_ind])

        labels = [s_data.ass_index, s_data.samp_index, s_data.rep_index]
        for i in range(
                s_data.value_index,
                len(new_active_attributes_list) +
                s_data.value_index):
            labels.append(i)

    else:
        labels = [s_data.ass_index, s_data.samp_index, s_data.rep_index]
        for i in range(
                s_data.value_index,
                len(activeAttributesList) +
                s_data.value_index):
            labels.append(i)

    if isinstance(plot_data, (CollectionCalcPlotData)):
        plot_data.collection_calc_data["accepted_active_attributes"] = new_active_attributes_list
    else:
        plot_data.accepted_active_attributes = new_active_attributes_list

    pathname = os.path.dirname(sys.argv[0])
    progPath = os.path.abspath(pathname)

    progress = Progress(None, progPath)
    progress.set_gauge(value=0, text="Using R...\n")

    # get program absolute-path:
    last_dir = os.getcwd()
    os.chdir(progPath)  # go to program path (for R script source)

    res = load_mm_anova_data(s_data, plot_data, abspath=abspath)
    os.chdir(last_dir)  # go back
    progress.set_gauge(value=100, text="Done\n")
    progress.Destroy()

    if one_rep:
        return res[1][1]  # Product Effect p-matrix
    else:
        return res[2][6]  # Product Effect p-matrix


def colored_frame(s_data, plot_data, active_att_list, active_att, abspath):
    if len(s_data.ReplicateList) == 1:
        one_rep = True
    else:
        one_rep = False

    # try:
    if isinstance(plot_data, (CollectionCalcPlotData)):
        # print("collection_calc")
        if not plot_data.collection_calc_data.__contains__("p_matr"):
            plot_data.collection_calc_data["p_matr"] = attribute_significance(
                s_data, plot_data, one_rep=one_rep, abspath=abspath)  # Product Effect p-matrix
        elif plot_data.collection_calc_data["p_matr"].size == 0:
            plot_data.collection_calc_data["p_matr"] = attribute_significance(
                s_data, plot_data, one_rep=one_rep, abspath=abspath)  # Product Effect p-matrix
        else:
            pass  # ok
        p_matr = plot_data.collection_calc_data["p_matr"]
    else:
        if not hasattr(plot_data, "p_matr"):
            plot_data.p_matr = attribute_significance(
                s_data, plot_data, one_rep=one_rep, abspath=abspath)  # Product Effect p-matrix
        elif 'None' in str(type(plot_data.p_matr)):
            plot_data.p_matr = attribute_significance(
                s_data, plot_data, one_rep=one_rep, abspath=abspath)  # Product Effect p-matrix
        else:
            pass  # ok
        p_matr = plot_data.p_matr

    lsd_colors = {
        0.0: '#999999',
        1.0: '#FFD800',
        2.0: '#FF8A00',
        3.0: '#E80B0B'}

    if isinstance(active_att_list[0], (int)):
        temp = []
        for ind in active_att_list:
            temp.append(s_data.AttributeList[ind])
        active_atts = temp
    else:
        active_atts = active_att_list

    if isinstance(plot_data, (CollectionCalcPlotData)):
        active_atts = plot_data.collection_calc_data["accepted_active_attributes"]
    elif isinstance(plot_data, (MM_ANOVA_PlotData)):
        active_atts = plot_data.accepted_active_attributes

    if p_matr.size == 0:
        print("Cannot set frame color: STD=0 for one or more attributes")
        return False
    elif len(p_matr) != len(active_atts):
        print(
            "Cannot set frame color: length of p list != length of active attributes list")
        return False

    if active_att not in active_atts:
        print("Cannot set frame color: active attribute index not valid")
        return False

    current_att_ind = active_atts.index(active_att)

    # set frame coloring:
    for spine in plot_data.ax.spines.values():
        spine.set_edgecolor(lsd_colors[p_matr[current_att_ind]])
        spine.set_linewidth(3)

    return True


def significance_legend(plot_data, pos='upper right'):
    # colors:   grey       yellow     orange      red
    _colors = ['#999999', '#FFD800', '#FF8A00', '#E80B0B']
    if plot_data.view_legend:
        plotList = []
        lables = ['', 'ns', 'p<0.05', 'p<0.01', 'p<0.001']
        # lables = ['ns','p<0.05','p<0.01','p<0.001']
        # i = 0
        for c in _colors:
            plotList.append(Line2D([], [], color=c, linewidth=5))
            # i += 1
        # import pdb; pdb.set_trace()
        figlegend = plot_data.fig.legend(
            plotList, lables, loc=pos, title='Prod. sign.\n (2-way ANOVA):')


############### General Plot Methods ###############

def OverviewPlotter(
        s_data,
        plot_data,
        itemID_list,
        plotter,
        current_list,
        special_selection=0,
        abspath=None):
    """
    Overview Plot
    """
    print("Overview plot (general method)")
    # print special_selection

    plot_data.overview_plot = True

    font = {'fontname': 'Arial Narrow',
            'color': 'black',
            'fontweight': 'normal',
            'fontsize': 9}

    num_plots = len(current_list)
    if num_plots == 0:
        show_err_msg('No plots to view. Check selections.')
        return

    num_edge = int(np.ceil(np.sqrt(num_plots)))
    # print num_edge

    c_list = current_list[:]
    progress = Progress(None, abspath)
    progress.set_gauge(value=0, text="Calculating...\n")
    part = int(np.floor(100 / num_plots))
    val = part

    # import pdb; pdb.set_trace()
    plot_data.tree_path = itemID_list[0]
    plot_data = plotter(
        s_data,
        plot_data,
        num_subplot=[
            num_edge,
            num_edge,
            1],
        selection=special_selection,
        abspath=abspath)

    txt = c_list[0] + " done\n"
    progress.set_gauge(value=val, text=txt)

    del c_list[0]

    if plot_data is None:
        progress.Destroy()
        print("Error: no plot data")
        return  # plotting failed

    fig = plot_data.fig  # will have multiple axes objects
    ax = plot_data.ax

    # text_element is matplotlib Text class
    if ax:
        for text_element in ax.get_xticklabels():
            text_element._fontproperties.set_size(9)
        for text_element in ax.get_yticklabels():
            text_element._fontproperties.set_size(9)
    # setp(ax.get_xticklabels(), fontsize=9)
    # setp(ax.get_yticklabels(), fontsize=9)
    num = 2
    for c_plot in c_list:
        plot_data.tree_path = itemID_list[num - 1]
        plot_data = plotter(
            s_data,
            plot_data,
            num_subplot=[
                num_edge,
                num_edge,
                num],
            selection=special_selection)

        ax = plot_data.ax  # pointer to last ax object added
        if ax:
            for text_element in ax.get_xticklabels():
                text_element._fontproperties.set_size(9)
            for text_element in ax.get_yticklabels():
                text_element._fontproperties.set_size(9)
            # setp(ax.get_xticklabels(), fontsize=9)
        # setp(ax.get_yticklabels(), fontsize=9)

        num += 1
        txt = c_plot + " done\n"
        val += part
        # print(val)
        progress.set_gauge(value=val, text=txt)

    progress.Destroy()

    if plot_data.view_legend:
        r = 0.8  # has legend
    else:
        r = 0.95

    plot_data.fig.subplots_adjust(
        left=0.05,
        bottom=0.05,
        right=r,
        top=0.95,
        wspace=0.15,
        hspace=0.3)

    return plot_data
