# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-06

why_am_i_doing_this.py
"""
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Data import
raw_dat = pd.read_excel("qap.xlsx")
dat = raw_dat.to_numpy()

# Conditionals
time_min = 600 # in seconds
short_qs = np.array(["DJ","DS"]) # columns in excel

# Helper functions that really should be in a module
def column_converter(col):
    """
    Converts excel column to usable indices.
    """
    num = 0
    for c in col:
        if isinstance(c, str):
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num - 1

def student_status(student: str):
    """
    Checks if a student responded to the grad and/or undergrad questions.
    """
    if isinstance(student[column_converter("I")], str) \
    or isinstance(student[column_converter("L")], str) \
    or isinstance(student[column_converter("CI")], str):
        if student[column_converter("I")] == "Graduate" \
        or student[column_converter("L")] == "Graduate":
            if student[column_converter("CI")] == "Yes":
                return "Both"
            else:
                return "Graduate"
        elif student[column_converter("I")] == "Undergraduate" \
        or student[column_converter("L")] == "Undergraduate":
            return "Undergraduate"
        else:
            return "Missing"
    else:
        return "Missing"
    
def alt_student_status(student: str) -> str:
    if isinstance(student[column_converter("CI")], str):
        if student[column_converter("CI")] == "Yes":
            return "Both"
        else:
            return "Graduate"
    elif student[column_converter("I")] == "Undergraduate"\
    or student[column_converter("L")] == "Undergraduate":
        return "Undergraduate"
    else:
        return "Missing"

def short_checker(response: str):
    """
    Checks short answers against criteria
    """
    if not isinstance(response, str): # removes blanks
        return False
    elif len(response) == 1: # removes single character responses
        return False
    return True
    
# P U R G E (Proper criteria not yet implemented)
bad = []
for i in dat:    
    # Time-based criteria
    if (i[2]-i[1]).total_seconds() < time_min:
        bad.append(i[0]-1)
        continue
    
    # Short-response criteria
    for j in short_qs:
        if not short_checker(i[column_converter(j)]):
            bad.append(i[0]-1)

results = np.delete(dat, np.array(bad), 0)
df_results = pd.DataFrame(data=results[0:,1:], index=results[0:,0], columns=np.array(raw_dat.columns)[1:])
df_results.to_excel("output.xlsx")
