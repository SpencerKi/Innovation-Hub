# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2023-02-28

"""
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

dept = 4#int(input("Please input the number corresponding to the department you are analysing:\n0: ART\n1: CSB\n2: EAS\n3: ESL\n4: HIS\n5: IR\n6: POL\n"))
if dept != 3 and dept != 5:
    stu = 0#int(input("Please input the number corresponding to the student status you would like to consider:\n0: All students and alumni\n1: Only current students\n2: Only alumni\n"))
    lvl = 2#int(input("Please input the number corresponding to the level of study you would like to consider:\n0: All levels of study\n1: Only undergraduate\n2: Only graduate students\n"))
    if lvl != 1:
        deg = 0#int(input("Please input the number corresponding to the graduate degress you would like to consider:\n0: All graduate degrees\n1: Only master's degrees\n2: Only PhDs\n"))
    else:
        deg = 0
else:
    stu = 0
    lvl = 0
    deg = 0

# Options for manually selecting filters; sub relevant dict keys into variables
department_options = {0: "ART", 1: "CSB", 2: "EAS", 3: "ESL", 4: "HIS", 5: "IR", 6: "POL"}
department = department_options[dept]

student_status_options = {0: "", 1: "Currently enrolled student", 2: "Alumnus"}
student_status = student_status_options[stu]

level_of_study_options = {0: "", 1: "Undergraduate", 2: "Graduate"}
level_of_study = level_of_study_options[lvl]

degree_options = {0: "", 1: "Master's", 2: "PhD"}
degree = degree_options[deg]

##############################################################################
# Indices for mapping to existing Excel columns
indices = {"ART": {"status": 169, "cur_lvl": 170, "alm_lvl": 7, "cur_dgr": 49, "alm_dgr": 189}, 
           "CSB": {"status": 5, "cur_lvl": 8, "alm_lvl": 11, "cur_dgr": 12, "alm_dgr": 12}, 
           "EAS": {"status": 4, "cur_lvl": 7, "alm_lvl": 10, "cur_dgr": 11, "alm_dgr": 11}, 
           "ESL": {"status": 8, "cur_lvl": 1000, "alm_lvl": 1000, "cur_dgr": 1000, "alm_dgr": 1000}, 
           "HIS": {"status": 186, "cur_lvl": 6, "alm_lvl": 187, "cur_dgr": 48, "alm_dgr": 48}, 
           "IR": {"status": 348, "cur_lvl": 1000, "alm_lvl": 1000, "cur_dgr": 1000, "alm_dgr": 1000}, 
           "POL": {"status": 5, "cur_lvl": 10, "alm_lvl": 8, "cur_dgr": 12, "alm_dgr": 8}}

# Import and filter data according to criteria in lines 13-26
raw_dat = pd.read_excel(f"{department}.xlsx")
dat = raw_dat
if student_status != "":
    dat = dat[(dat[dat.iloc[:,indices[department]["status"]].name] == student_status)]
if level_of_study != "":
    dat = dat[(dat[dat.iloc[:,indices[department]["cur_lvl"]].name] == "Graduate Student") | 
              (dat[dat.iloc[:,indices[department]["alm_lvl"]].name] == level_of_study)]
if degree != "":
    dat = dat[(dat[dat.iloc[:,indices[department]["cur_dgr"]].name] == degree) | 
              (dat[dat.iloc[:,indices[department]["alm_dgr"]].name] == degree)]# |
              #(dat[dat.iloc[:,33].name] == "Yes")]
dat = dat.to_numpy()

# Quantify Likert questions according to regex criteria
for i in range(len(dat)):
    for j in range(len(dat.T)):
        if type(dat[i][j]) == str:
            if bool(re.search("^Not at all.*", dat[i][j])) \
                or bool(re.match("Poor", dat[i][j])) \
                    or bool(re.match("Definitely no", dat[i][j])) \
                        or bool(re.match("No", dat[i][j])) \
                            or bool(re.match("Strongly disagree", dat[i][j])):
                dat[i][j] = 0.0
            elif bool(re.search("^Slightly.*", dat[i][j])) \
                or bool(re.match("Probably no", dat[i][j])) \
                    or bool(re.match("Unlikely", dat[i][j])) \
                        or bool(re.match("Disagree", dat[i][j])):
                dat[i][j] = 1.0
            elif bool(re.search("^Moderately.*", dat[i][j])) \
                or bool(re.match("Fair", dat[i][j])) \
                    or bool(re.match("Neither agree nor disagree", dat[i][j])):
                dat[i][j] = 2.0
            elif bool(re.search("^Very.*", dat[i][j]))\
                or bool(re.match("Good", dat[i][j])) \
                    or bool(re.match("Probably yes", dat[i][j])) \
                        or bool(re.match("Likely", dat[i][j])) \
                            or bool(re.match("Agree", dat[i][j])):
                dat[i][j] = 3.0
            elif bool(re.search("^Extremely.*", dat[i][j])) \
                or bool(re.match("Excellent", dat[i][j])) \
                    or bool(re.match("Definitely yes", dat[i][j])) \
                        or bool(re.match("Yes", dat[i][j])) \
                            or bool(re.match("Very likely", dat[i][j])) \
                                or bool(re.match("Strongly Agree", dat[i][j])):
                dat[i][j] = 4.0
            elif bool(re.search("Does not [Aa]pply", dat[i][j])) \
                or bool(re.match("Unsure", dat[i][j])) \
                    or bool(re.match("Had no contact/Did not use", dat[i][j])):
                dat[i][j] = np.nan
            elif bool(re.search("^[0-9].{3}year", dat[i][j])):
                dat[i][j] = float(dat[i][j][0])

# Tag and calculate sample statistics for columns with valid datatypes and inputs
valid_qs = {}
for i in range(len(dat.T)):
    try:
        dat.T[i].astype(float)
        if np.count_nonzero(~np.isnan(dat.T[i].astype(float))) > 0:
            valid_qs[i] = raw_dat.columns[i]
    except:
        continue

prompt = [list(x) for x in list(valid_qs.items())]
prompt = [f"{x[0]}: {x[1]}" for x in prompt]

display_qs = input("PLEASE ENTER THE NUMBERS OF THE QUESTIONS YOU WANT INCLUDED IN THE VISUALISATION, SEPARATED BY COMMAS:\n\n" + "\n\n".join(prompt) + "\n\nSCROLL UP TO SEE INSTRUCTIONS NEAR THE TOP\n")
display_qs = display_qs.split(",")
display_qs = [int(x.strip()) for x in display_qs]

results = {}
for i in display_qs:
    unique, counts = np.unique(dat.T[i].astype(float), return_counts=True)
    ref = dict(zip(unique.astype(str), counts))
    if "0.0" not in ref:
        ref["0.0"] = 0
    if "1.0" not in ref:
        ref["1.0"] = 0
    if "2.0" not in ref:
        ref["2.0"] = 0
    if "3.0" not in ref:
        ref["3.0"] = 0
    if "4.0" not in ref:
        ref["4.0"] = 0
    if "nan" not in ref:
        ref["nan"] = 0
    results[raw_dat.columns[i]] = [
        round(ref["4.0"]/dat.T[i].shape[0]*100), 
        round(ref["3.0"]/dat.T[i].shape[0]*100), 
        round(ref["2.0"]/dat.T[i].shape[0]*100), 
        round(ref["1.0"]/dat.T[i].shape[0]*100), 
        round(ref["0.0"]/dat.T[i].shape[0]*100), 
        round(ref["nan"]/dat.T[i].shape[0]*100)]
    
for i in results:
    if sum(results[i]) != 100:
        results[i][-1] +=  100 - sum(results[i])

categories = input("Which of the following categories fit the data:\n\n1: [0: Not at all, 1: Slightly, 2: Moderately, 3: Very, 4: Extremely]\n\n2: [0: Poor, 2: Fair, 3: Good, 4: Excellent]\n\n3: [0: Definitely no, 1: Probably no, 3: Probably yes, 4: Definitely yes]\n")

if categories == "1":
    category_names = ["Extremely", "Very", "Moderately","Slightly", "Not at all", "No response"]
elif categories == "2":
    category_names = ["Excellent", "Good", "Fair", "Poor", "No response"]
    for i in results:
        del results[i][3]
elif categories == "3":
    category_names = ["Definitely yes", "Probably yes", "Probably no", "Definitely no", "No response"]
    for i in results:
        del results[i][2]
elif categories == "4":
    category_names = ["Yes", "No", "No response"]
    for i in results:
        del results[i][1:4]
elif categories == "5":
    category_names = ["Very", "Moderately","Slightly", "Not at all", "No response"]
    for i in results:
        del results[i][0]
elif categories == "6":
    category_names = ["Very likely", "Likely", "Unlikely", "Not at all", "No response"]
    for i in results:
        del results[i][2]
elif categories == "7":
    category_names = ["Strongly agree", "Agree", "Neither agree nor disagree", "Disagree", "Strongly disagree", "No response"]
else:
    category_names = ["Extremely", "Very", "Moderately","Slightly", "Not at all", "No response"]

title = input("WHAT IS THE OVERARCHING QUESTION OF THIS VISUALISATION (e.g., How important were the following factors to you in deciding on your program of study?)?\n")

def survey(results, category_names, title):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
        
    https://matplotlib.org/stable/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    """
    holder = np.array([w[:int(len(w)/2)+2] if len(w) > 100 else w for w in list(results.keys())])
    labels = []
    for i in holder:
        if len(i.split(" ")) > 3:
            arrs = np.array_split(np.array(i.split(" ")), 2)
            end_word = []
            for j in arrs:
                end_word.append(" ".join(j))
            labels.append("\n".join(end_word) + "...")
        else:
            labels.append(i)
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['summer'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)
        blabels_threshold = 5
        blabels = [str(v)+"%" if v > blabels_threshold else "" for v in rects.datavalues]  

        r, g, b, _ = color
        text_color = 'black'#'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, labels=blabels, label_type='center', color=text_color)
    ax.legend(ncol = len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')
    
    fig.suptitle(f"{title} (n = {dat.shape[0]})")
    fig.supxlabel("Proportional response rate (%)")
    fig.supylabel("Options")

    return fig

graph = survey(results, category_names, title)
plt.tight_layout()
graph.show()
filename = "_".join([option for option in [department, level_of_study, degree, student_status] if option != ""])
graph.savefig(f"{filename}_{title[:-1]}.png")
graph.savefig(f"{filename}_{title[:-1]}.svg")

# new_results = {"Service-learning courses" : results[list(results.keys())[0]],
#                "Active-learning courses" : results[list(results.keys())[1]],
#                "Research participation courses" : results[list(results.keys())[2]]}
# title = "How interested are you in the following types of courses:"