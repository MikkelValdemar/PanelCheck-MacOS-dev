#!/usr/bin/env python
# -------------------------------------------------------------------------------
# Name:        rawData_Plot.py
# Purpose:     Plotting the attribute mean and attribute STD for one assessor.
#              Plotting the assessor mean and assessor STD for one attribute.
# -------------------------------------------------------------------------------

#from scripts.Plot_Tools import *
import wx
import numpy as np
from matplotlib.figure import Figure
from Math_Tools import STD
from Plot_Tools import OverviewPlotter, set_xlabeling, num2str, axes_create, assign_colors, axes_setup, set_xlabeling_rotation, raw_data_grid, colored_frame, significance_legend

def RawDataAssessorPlotter(s_data, plot_data, num_subplot=[1, 1, 1], abspath=None, **kwargs):

    activeAssessorsList = plot_data.activeAssessorsList
    activeAttributesList = plot_data.activeAttributesList
    activeSamplesList = plot_data.activeSamplesList
    itemID = plot_data.tree_path

    # list checks
    if itemID[0] not in activeAssessorsList:  # no active assessors
        dlg = wx.MessageDialog(None, 'Assessor is not active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return
    if len(activeAttributesList) < 1:  # no active assessors
        dlg = wx.MessageDialog(None, 'No attributes are active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return
    if len(activeSamplesList) < 1:  # no active samples
        dlg = wx.MessageDialog(None, 'No samples are active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    # Dictionaries and matrix where numbers will be stored in
    results = {}
    resultList = []
    specSparseMatrix = {}
    tempMatrix = np.zeros((1, len(s_data.AttributeList)), float)

    # Loop through all active samples for the specific assessor
    for sample in activeSamplesList:

        for replicate in s_data.ReplicateList:

            # Fetch the required data from sparse matrix
            _object = s_data.SparseMatrix[(itemID[0], sample, replicate)]

            # Transforming scores that are strings to floats.
            newObject = []
            for number in _object:
                newObject.append(float(number))

            # Transforming 'newObject' to matrix (NOT array) to avoid problems
            # with dimensions and vstack.
            newObject = np.mat(newObject)
            tempMatrix = np.vstack((tempMatrix, newObject))
            specSparseMatrix[(itemID[0], sample, replicate)] = np.array(newObject)

    # Transforming matrix back to array and removing first row with zeros
    tempMatrix = np.array(tempMatrix)
    tempMatrix = tempMatrix[1:, :]

    # Create list that holds the index of each active attribute in
    # attributeList
    columns = []
    for att in s_data.AttributeList:
        if att in activeAttributesList:
            columns.append(s_data.AttributeList.index(att))

    # New matrix with active attributes
    specMatrix = np.take(tempMatrix, columns, 1)

    # Compute averages and STD's
    averages = np.average(specMatrix, 0)
    # print averages
    standDevs = STD(specMatrix, 0)
    # print "std"
    # print standDevs
    # Store results in results dictionary
    results['averages'] = averages
    results['STDs'] = standDevs
    results['specSparseMatrix'] = specSparseMatrix
    results['D'] = specMatrix

    emptyLine = ['']

    rawDataList = raw_data_grid(s_data, plot_data, [itemID[0]])

    results['averages'] = averages
    results['STDs'] = standDevs
    results['specSparseMatrix'] = specSparseMatrix

    resultList = []
    resultList.append([itemID[0]])
    resultList.append([""])
    resultList.append(["Averages:"])
    resultList.append(activeAttributesList)
    _line = []
    for x in averages:
        _line.append(num2str(x, fmt="%.2f"))
    resultList.append(_line)
    resultList.append([""])
    resultList.append(["STDs:"])
    resultList.append(activeAttributesList)
    _line = []
    for x in standDevs:
        _line.append(num2str(x, fmt="%.2f"))
    resultList.append(_line)
    resultList.append([""])

    plot_data.view_legend = False

    # Figure
    replot = False
    subplot = plot_data.overview_plot
    if plot_data.fig is not None:
        replot = True
    else:
        plot_data.fig = Figure(None)
    if subplot:  # is subplot
        plot_data.ax = plot_data.fig.add_subplot(
            num_subplot[0], num_subplot[1], num_subplot[2])
    else:
        plot_data.ax = axes_create(0, plot_data.fig)
    ax = plot_data.ax
    fig = plot_data.fig

    # plotting:
    x_values = np.arange(1, len(averages) + 1)
    width = 0.35
    ax.bar(x_values - (width / 2), averages,
           width, color='#FF0000', yerr=standDevs)

    pointAndLabelList = []
    for i in range(len(activeAttributesList)):
        label = activeAttributesList[i] + ": Average=" + \
            str(averages[i]) + ", STD=" + str(standDevs[i])
        pointAndLabelList.append([x_values[i], averages[i], label])

    ax.grid(plot_data.view_grid)

    _title = "Mean & STD Plot: " + itemID[0]
    limits = plot_data.limits
    if len(activeAttributesList) > 7:
        set_xlabeling_rotation(ax, 'vertical', fontsize=10)

    if not subplot:
        axes_setup(
            ax, 'Attributes', 'Score', _title, [
                0, len(activeAttributesList) + 1, 0, limits[3]])
        set_xlabeling(ax, activeAttributesList)
    else:
        axes_setup(
            ax, '', '', _title, [
                0, len(activeAttributesList) + 1, 0, limits[3]], font_size=10)
        set_xlabeling(ax, np.arange(1, len(activeAttributesList) + 1))

    # update plot-data variables:
    plot_data.point_label_line_width = width * 0.5
    plot_data.point_lables = pointAndLabelList
    plot_data.raw_data = rawDataList
    plot_data.numeric_data = resultList
    plot_data.plot_type = "mean_std_ass"
    plot_data.point_lables_type = 1

    # Frame draw, for standard Matplotlib frame only use show()
    return plot_data


def RawDataAttributePlotter(
        s_data,
        plot_data,
        num_subplot=[
            1,
            1,
            1],
        abspath=None,
        **kwargs):
    activeAssessorsList = plot_data.activeAssessorsList
    activeAttributesList = plot_data.activeAttributesList
    activeSamplesList = plot_data.activeSamplesList
    itemID = plot_data.tree_path

    # list checks
    if itemID[0] not in activeAttributesList:  # no active assessors
        dlg = wx.MessageDialog(None, 'Attribute is not active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return
    if len(activeAssessorsList) < 1:  # no active assessors
        dlg = wx.MessageDialog(None, 'No attributes are active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return
    if len(activeSamplesList) < 1:  # no active samples
        dlg = wx.MessageDialog(None, 'No samples are active in CheckBox',
                               'Error Message',
                               wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    # Dictionaries and matrix where numbers will be stored in
    results = {}
    specSparseMatrix = {}
    tempMatrix = np.zeros((1, len(s_data.AssessorList)), float)

    attIndex = s_data.AttributeList.index(itemID[0])
    # print attIndex

    # Construct a list that holds the scores of the active assessors for the
    # active samples. The score of each assessors are stored in lists, too.
    attributeVectors = []
    for ass in activeAssessorsList:

        assessorVector = []
        for samp in activeSamplesList:

            for rep in s_data.ReplicateList:

                value = float(s_data.SparseMatrix[(ass, samp, rep)][attIndex])
                assessorVector.append(value)

        attributeVectors.append(assessorVector)

    # Turn list holding lists into an array
    attributeArray = np.array(attributeVectors)

    # Compute averages and STD's
    averages = np.average(attributeArray, 1)
    standDevs = STD(attributeArray, 1)

    # Store results in results dictionary
    results['averages'] = averages
    results['STDs'] = standDevs

    emptyLine = ['']

    rawDataList = raw_data_grid(s_data, plot_data)

    # Store results in results dictionary
    results['averages'] = averages
    results['STDs'] = standDevs
    results['specSparseMatrix'] = specSparseMatrix

    resultList = []
    resultList.append([itemID[0]])
    resultList.append([""])
    resultList.append(["Averages:"])
    resultList.append(activeAssessorsList)
    _line = []
    for x in averages:
        _line.append(num2str(x, fmt="%.2f"))
    resultList.append(_line)
    resultList.append([""])
    resultList.append(["STDs:"])
    resultList.append(activeAssessorsList)
    _line = []
    for x in standDevs:
        _line.append(num2str(x, fmt="%.2f"))
    resultList.append(_line)
    resultList.append([""])

    view_legend = plot_data.view_legend

    # Figure
    replot = False
    subplot = plot_data.overview_plot
    scatter_width = 35
    if plot_data.fig is not None:
        replot = True
    else:
        plot_data.fig = Figure(None)
    if subplot:  # is subplot
        plot_data.ax = plot_data.fig.add_subplot(
            num_subplot[0], num_subplot[1], num_subplot[2])
        scatter_width = 15
    else:
        plot_data.ax = axes_create(view_legend, plot_data.fig)
    ax = plot_data.ax
    fig = plot_data.fig

    # plotting:
    _colors = assign_colors(s_data.AssessorList, ["rep"])
    colors = []
    for ass in activeAssessorsList:
        colors.append(_colors[(ass, "rep")][0])

    x_values = np.arange(1, len(averages) + 1)
    width = 0.35
    ax.bar(x_values - (width / 2), averages,
           width, color="#00DD00", yerr=standDevs)

    ax.grid(plot_data.view_grid)

    pointAndLabelList = []
    for i in range(len(activeAssessorsList)):
        label = activeAssessorsList[i] + ": Average=" + \
            str(averages[i]) + ", STD=" + str(standDevs[i])
        pointAndLabelList.append([x_values[i], averages[i], label])

    _title = "Mean & STD Plot: " + itemID[0]
    limits = plot_data.limits

    if len(activeAssessorsList) > 7:
        set_xlabeling_rotation(ax, 'vertical', fontsize=10)

    if not subplot:
        axes_setup(
            ax, 'Assessors', 'Score', _title, [
                0, len(activeAssessorsList) + 1, 0, limits[3]])
        set_xlabeling(ax, activeAssessorsList)
    else:
        axes_setup(
            ax, '', '', _title, [
                0, len(activeAssessorsList) + 1, 0, limits[3]], font_size=10)
        set_xlabeling(ax, np.arange(1, len(activeAssessorsList) + 1))

    # TODO MVK: Fix colored frame
    frame_colored = colored_frame(
        s_data,
        plot_data,
        activeAttributesList,
        itemID[0],
        abspath)

    if frame_colored:
        significance_legend(plot_data)

    # update plot-data variables:
    plot_data.point_label_line_width = width * 0.5
    plot_data.point_lables = pointAndLabelList
    plot_data.point_lables_type = 1
    plot_data.raw_data = rawDataList
    plot_data.numeric_data = resultList
    plot_data.plot_type = "mean_std_att"
    # plot_data.fig.legend.title='asd'
    # Frame draw, for standard Matplotlib frame only use show()
    return plot_data

def RawDataAssessorOverviewPlotter(s_data, plot_data, abspath, **kwargs):
    itemID_list = []  # takes part in what to be plotted
    for ass in plot_data.activeAssessorsList:
        itemID_list.append([ass])
    return OverviewPlotter(
        s_data,
        plot_data,
        itemID_list,
        RawDataAssessorPlotter,
        plot_data.activeAssessorsList,
        abspath=abspath)

def RawDataAttributeOverviewPlotter(s_data, plot_data, abspath, **kwargs):
    itemID_list = []  # takes part in what to be plotted
    for att in plot_data.activeAttributesList:
        itemID_list.append([att])
    return OverviewPlotter(
        s_data,
        plot_data,
        itemID_list,
        RawDataAttributePlotter,
        plot_data.activeAttributesList,
        abspath=abspath)
