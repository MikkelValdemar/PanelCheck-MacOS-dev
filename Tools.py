import wx
import re
import os
import sys
import codecs


# from Progress_Info import Progress
# from Summary import SummaryFrame
# from Grid import *
#
# from PanelCheck_IO import *


def split_path(abs_path):
    """
    Returns tuple with: (directory-path, filename, file_extension)
    """
    if os.name == 'nt':  # windows (same on a 'ce' system?)
        match = re.search(r"(.*)/(.*)\.(.*)", abs_path)
    else:  # hopefully some unix system (not sure about how it looks on mac)
        match = re.search(r"(.*)/(.*)\.(.*)", abs_path)
    return match.groups()
    # three items in a tuple: ('directory-path', 'filename', 'file-extension')
#
#
def summaryConstructor(self, sampleList, assessorList, replicateList,
                       attributeList):
    """
    Creates summary text of given lists.

    @type sampleList:     list
    @param sampleList:    Complete list of ALL samples

    @type assessorList:     list
    @param assessorList:    Complete list of ALL assessors

    @type replicateList:    list
    @param replicateList:   Complete list of ALL replicates

    @type attributeList:    list
    @param attributeList:   Complete list of ALL attributes
    """
    # TODO: Recognition of which plotting methods are possible based on number
    # of replicates

    infoString = 'Number of assessors:   ' + str(len(assessorList)) + \
        '\n=================\n\n'

    for assessor in assessorList:
        infoString = infoString + str(assessorList.index(assessor) + 1) + \
            ': ' + assessor + '\n'

    infoString = infoString + '\n\n\n'

    infoString = infoString + 'Number of samples:   ' + \
        str(len(sampleList)) + '\n================\n\n'

    for sample in sampleList:
        infoString = infoString + str(sampleList.index(sample) + 1) + \
            ': ' + sample + '\n'

    infoString = infoString + '\n\n\n'

    infoString = infoString + 'Number of replicates:   ' + \
        str(len(replicateList)) + '\n================\n\n'

    infoString = infoString + '\n\n\n'

    infoString = infoString + 'Number of attributes:   ' + \
        str(len(attributeList)) + '\n================\n\n'

    for attribute in attributeList:
        infoString = infoString + str(attributeList.index(attribute) + 1) + \
            ': ' + attribute + '\n'

    return infoString


def summaryConstructor2(self, sampleList, assessorList, replicateList,
                        attributeList, mv_inf, summary):
    """
    Creates summary text of given lists.

    @type sampleList:     list
    @param sampleList:    Complete list of ALL samples

    @type assessorList:     list
    @param assessorList:    Complete list of ALL assessors

    @type replicateList:    list
    @param replicateList:   Complete list of ALL replicates

    @type attributeList:    list
    @param attributeList:   Complete list of ALL attributes
    """
    # TODO: Recognition of which plotting methods are possible based on number
    # of replicates

    infoString = 'Number of assessors:   ' + \
        str(len(assessorList)) + '\n=================\n\n'
    str_ind = summary.str_ind + len(infoString)

    txt_ctrl = summary.textSummary3

    txt_ctrl.AppendText(infoString)
    txt_ctrl.SetInsertionPoint(0)

    #print("\tIN SUMMARY CONTRUCTOR 2")
    # print(assessorList)
    # print(sampleList)
    # print(replicateList)
    # print(mv_inf)

    for assessor in assessorList:
        missing = "(No missing values)"
        color = "BLUE"
        # print("ASDASD"*2,assessor,"21312312"*2)
        # print(mv_inf)
        if mv_inf[assessor] > 0:
            missing = "(%.2f" % (mv_inf[assessor] * 100.0)
            missing += "% missing values)"
            color = "RED"
        infoString = str(assessorList.index(assessor) + 1) + \
            ': ' + assessor + '   '
        infoString = infoString + missing + '\n'
        str_ind += len(infoString)
        txt_ctrl.AppendText(infoString)
        txt_ctrl.SetStyle(
            str_ind - len(missing) - 1,
            str_ind - 1,
            wx.TextAttr(color))

    infoString = '\n\n\n'

    infoString = infoString + 'Number of samples:   ' + \
        str(len(sampleList)) + '\n================\n\n'

    for sample in sampleList:
        infoString = infoString + str(sampleList.index(sample) + 1) + \
            ': ' + sample + '\n'

    infoString = infoString + '\n\n\n'

    infoString = infoString + 'Number of replicates:   ' + \
        str(len(replicateList)) + '\n================\n\n'

    infoString = infoString + '\n\n\n'

    infoString = infoString + 'Number of attributes:   ' + \
        str(len(attributeList)) + '\n================\n\n'

    for attribute in attributeList:
        infoString = infoString + str(attributeList.index(attribute) + 1) + \
            ': ' + attribute + '\n'

    txt_ctrl.AppendText(infoString)
    txt_ctrl.SetInsertionPoint(0)
    txt_ctrl.Refresh()
    txt_ctrl.Update()

#
# # system encoding:
# encoding1 = sys.getfilesystemencoding()  # can be:   'mbcs' win32
# # can be:   'cp850' win32 extended latin-1 type
# encoding2 = sys.stdin.encoding
# encoding3 = sys.getdefaultencoding()   # usually:  'ascii'
#
# codec = encoding1
#
# # setting encoder and decoder:
# try:
#     enc, dec = codecs.lookup(encoding1)[:2]
# except LookupError:
#     enc, dec = codecs.lookup(encoding2)[:2]
#     codec = self.encoding2
# except LookupError:
#     enc, dec = codecs.lookup('latin-1')[:2]
#     codec = 'latin-1'
# except LookupError:
#     enc, dec = codecs.lookup('utf-8')[:2]
#     codec = 'utf-8'
# except LookupError:
#     enc, dec = codecs.lookup(encoding3)[:2]  # most likely using 'ascii'
#     codec = encoding3
#
#
# def safe_uni_dec(obj):
#     """
#     returns the decoded unicode representation of obj
#     """
#     try:
#         #uni = self.dec(obj)[0]
#         # print "unicode type string: " + self.enc(uni)[0] # may return: UnicodeEncodeError
#         # return uni
#         return dec(obj)[0]
#     except UnicodeDecodeError:  # cannot handle characters with code table
#         # print 'UnicodeDecodeError: trying with "replace"..'
#         return unicode(obj, codec, 'replace')
#     except UnicodeDecodeError:  # cannot handle characters with code table
#         # print 'UnicodeDecodeError: trying with "replace" and with
#         # sys.stdin.encoding'
#         codec = encoding2
#         return unicode(obj, codec, 'replace')
#     except UnicodeDecodeError:
#         # print 'UnicodeDecodeError: cannot decode'
#         return str(obj)
#     except UnicodeEncodeError:
#         return enc(obj)[0]
#     except BaseException:
#         return obj.encode('ascii', 'ignore')
#
#
# def safe_uni_enc(obj):
#     """
#     returns the decoded unicode representation of obj
#     """
#     try:
#         # trying to encode (transform from "natural" into "artificial") with
#         # known encoding 'sys.getfilesystemencoding()'
#         uni = enc(obj)[0]
#         # returning decoded (to "natural" unicode representation)
#         return dec(uni)[0]
#     except UnicodeEncodeError:  # cannot handle characters with code table
#         # print 'UnicodeEncodeError: trying with "replace"..'
#         uni = obj.encode(codec, 'replace')
#         return unicode(uni, codec, 'replace')
#     except UnicodeEncodeError:  # cannot handle characters with code table
#         # print 'UnicodeEncodeError: trying with "replace" and with
#         # sys.stdin.encoding'
#         codec = encoding2
#         uni = obj.encode(codec, 'replace')
#         return unicode(uni, codec, 'replace')
#     except UnicodeEncodeError:
#         # print 'UnicodeEncodeError: cannot encode'
#         return str(obj)
#     except UnicodeDecodeError:
#         return safe_uni_dec(obj)
#
#
def save_dataset(abspath, dataset):
    """
    Saves a dataset as a standard PanelCheck file
    """

    try:
        f = open(abspath, 'w')

        f.write("Assessor\tSample\tReplicate\t")
        for att in dataset.AttributeList:
            if att == dataset.AttributeList[-1]:
                f.write(att)
            else:
                f.write(att + "\t")
        f.write("\n")

        for ass in dataset.AssessorList:
            for samp in dataset.SampleList:
                for rep in dataset.ReplicateList:
                    f.write(
                        ass +
                        "\t" +
                        samp +
                        "\t" +
                        rep +
                        "\t")
                    for i in range(len(dataset.AttributeList)):
                        if i >= len(dataset.AttributeList) - 1:
                            f.write(
                                str(dataset.SparseMatrix[(ass, samp, rep)][i]))
                        else:
                            f.write(
                                str(dataset.SparseMatrix[(ass, samp, rep)][i]) + "\t")
                    f.write("\n")
        f.close()

        return "Dataset saved as: " + abspath

    except BaseException:
        import traceback
        print(traceback.print_exc())
        return traceback.format_exc()
