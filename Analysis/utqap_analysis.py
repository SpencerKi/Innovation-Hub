# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2023-02-28
Quantify UTQAP Likert responses and return relevant statistics via Excel.
"""
import numpy as np
import pandas as pd
import re
from scipy.stats import skew, mode

# User prompts (for app export; comment out for script use)
dept = int(input("Please input the number corresponding to the department you are analysing:\n0: ART\n1: CSB\n2: EAS\n3: ESL\n4: HIS\n5: IR\n6: POL\n"))
stu = int(input("Please input the number corresponding to the student status you would like to consider:\n0: All students and alumni\n1: Only current students\n2: Only alumni\n"))
lvl = int(input("Please input the number corresponding to the level of study you would like to consider:\n0: All levels of study\n1: Only undergraduate\n2: Only graduate students\n"))
if lvl != 1:
    deg = int(input("Please input the number corresponding to the graduate degress you would like to consider:\n0: All graduate degrees\n1: Only master's degrees\n2: Only PhDs\n"))
else:
    deg = 0
cort = float(input("Please enter the minimum correlation between variables you would like to flag:\n"))

# Options for manually selecting filters; sub relevant dict keys into variables
department_options = {0: "ART", 1: "CSB", 2: "EAS", 3: "ESL", 4: "HIS", 5: "IR", 6: "POL"}
department = dept

student_status_options = {0: "", 1: "Currently enrolled student", 2: "Alumnus"}
student_status = stu

level_of_study_options = {0: "", 1: "Undergraduate", 2: "Graduate"}
level_of_study = lvl

degree_options = {0: "", 1: "Master's", 2: "PhD"}
degree = deg

correlation_threshold = cort
proportion_threshold = 0.2# Minimum sample proportion for analysis

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
    dat = dat[(dat[dat.iloc[:,indices[department]["cur_lvl"]].name] == level_of_study) | 
              (dat[dat.iloc[:,indices[department]["alm_lvl"]].name] == level_of_study)]
if degree != "":
    dat = dat[(dat[dat.iloc[:,indices[department]["cur_dgr"]].name] == degree) | 
              (dat[dat.iloc[:,indices[department]["alm_dgr"]].name] == degree)]
dat = dat.to_numpy()

# Quantify Likert questions according to regex criteria
for i in range(len(dat)):
    for j in range(len(dat.T)):
        if type(dat[i][j]) == str:
            if bool(re.search("^Not at all.*", dat[i][j])) \
                or bool(re.match("Poor", dat[i][j])) \
                    or bool(re.match("Definitely no", dat[i][j])):
                dat[i][j] = 0.0
            elif bool(re.search("^Slightly.*", dat[i][j])) \
                or bool(re.match("Probably no", dat[i][j])):
                dat[i][j] = 1.0
            elif bool(re.search("^Moderately.*", dat[i][j])) \
                or bool(re.match("Fair", dat[i][j])):
                dat[i][j] = 2.0
            elif bool(re.search("^Very.*", dat[i][j]))\
                or bool(re.match("Good", dat[i][j])) \
                    or bool(re.match("Probably yes", dat[i][j])):
                dat[i][j] = 3.0
            elif bool(re.search("^Extremely.*", dat[i][j])) \
                or bool(re.match("Excellent", dat[i][j])) \
                    or bool(re.match("Definitely yes", dat[i][j])):
                dat[i][j] = 4.0
            elif bool(re.search("Does not [Aa]pply", dat[i][j])) \
                or bool(re.match("Unsure", dat[i][j])):
                dat[i][j] = np.nan
            elif bool(re.search("^[0-9].{3}year", dat[i][j])):
                dat[i][j] = float(dat[i][j][0])

# Tag and calculate sample statistics for columns with valid datatypes and inputs
valid_qs = []
stats = []
results = {}
for i in range(len(dat.T)):
    try:
        dat.T[i].astype(float)
        if np.count_nonzero(~np.isnan(dat.T[i].astype(float))) > 0:
            valid_qs.append(i)
            stats.append([raw_dat.columns[i], 
                          np.count_nonzero(~np.isnan(dat.T[i].astype(float))), 
                          np.nanmean(dat.T[i].astype(float)), 
                          np.nanmedian(dat.T[i].astype(float)), 
                          mode(dat.T[i].astype(float), nan_policy = "omit"), 
                          np.nanstd(dat.T[i].astype(float)), 
                          skew(dat.T[i].astype(float), nan_policy = "omit")])
    except:
        continue

# Create 'correlation matrix' of columns that correlate over the given thresholds
correlated = []
for i in range(len(valid_qs)):
    a = np.ma.masked_invalid(dat.T[valid_qs[i]].astype(float))
    for j in range(i+1, len(valid_qs)):
        b = np.ma.masked_invalid(dat.T[valid_qs[j]].astype(float))
        msk = (~a.mask & ~b.mask)
        cor = np.ma.corrcoef(a[msk],b[msk])[0][-1]
        if np.abs(cor) >= correlation_threshold \
            and sum(msk) >= proportion_threshold * dat.shape[0]:
            correlated.append([raw_dat.columns[valid_qs[i]], 
                               raw_dat.columns[valid_qs[j]], 
                               sum(msk), 
                               cor])

# Export calculations to Excel
cor_header = [["Question 1", "Question 2", "Sample Size", "Correlation"]]
cor_output = pd.DataFrame(cor_header + correlated)
stats_header = [["Question", "Sample Size", "Mean", "Median", "Mode", "Standard Deviation", "Skew"]]
stats_output = pd.DataFrame(stats_header + stats)
filename = "_".join([option for option in [department, level_of_study, degree, student_status] if option != ""])
with pd.ExcelWriter(f"{filename}_analysis.xlsx") as writer:
    stats_output.to_excel(writer, sheet_name = "Statistics", header = False, index = False)
    cor_output.to_excel(writer, sheet_name = "Correlations", header = False, index = False)