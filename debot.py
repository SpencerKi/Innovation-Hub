# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-07

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

# Helper functions that really should be in a module
def col_conv(col) -> float:
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
    Checks how a student responded to the grad and/or undergrad questions.
    """
    if isinstance(student[col_conv("I")], str) \
    or isinstance(student[col_conv("L")], str):
        if student[col_conv("I")] == "Graduate" \
        or student[col_conv("L")] == "Graduate":
            if student[col_conv("CI")] == "Yes":
                return "Both"
            elif student[col_conv("CI")] == "No":
                return "Graduate"
            else:
                return "Missing"
        elif student[col_conv("I")] == "Undergraduate" \
        or student[col_conv("L")] == "Undergraduate":
            return "Undergraduate"
        else:
            return "Missing"
    else:
        return "Missing"

def fetch_stats(df: pd.DataFrame, q: str):
    return df.iloc()[:,col_conv(q)].describe()

# Priority Control 1

# Conditionals
complete_min = 600 # in seconds
grad_short_qs = np.array(["CE","CH"]) # columns in excel
ug_short_qs = np.array(["CZ","DJ","DS","EJ"])

def short_checker(response: str) -> bool:
    """
    Checks short answers against criteria
    """
    if not isinstance(response, str): # removes blanks
        return False
    elif len(response) == 1: # removes single character responses
        return False
    return True

bad = []
for i in dat:   
    completion_time = (i[2]-i[1]).total_seconds()

    # General time-based criteria
    if completion_time < complete_min:
        bad.append(i[0]-1)
        continue
    
    # Student-status criteria
    stat = student_status(i)
    if stat == "Missing":
        bad.append(i[0]-1)
        continue
    elif stat == "Graduate":
        for j in grad_short_qs:
            if not short_checker(i[col_conv(j)]):
                bad.append(i[0]-1)
                break
        continue
    elif stat == "Undergraduate":
        for j in ug_short_qs:
            if not short_checker(i[col_conv(j)]):
                bad.append(i[0]-1)
                break
        continue
    elif stat == "Both":
        for j in np.concatenate((grad_short_qs, ug_short_qs)):
            if not short_checker(i[col_conv(j)]):
                bad.append(i[0]-1)
                break
        continue

# # Priority Control 2

# # Conditionals
# complete_min = 360 # in seconds
# grad_short_qs = np.array(["CE","CH"]) # columns in excel
# ug_short_qs = np.array(["CZ","DJ","DS","EJ"])

# def short_checker(response: str) -> bool:
#     """
#     Checks short answers against criteria
#     """
#     if not isinstance(response, str): # removes blanks
#         return False
#     elif len(response) == 1: # removes single character responses
#         return False
#     return True

# bad = []
# for i in dat:   
#     completion_time = (i[2]-i[1]).total_seconds()

#     # General time-based criteria
#     if completion_time < complete_min:
#         bad.append(i[0]-1)
#         continue
    
#     # Studen-status criteria
#     stat = student_status(i)
#     resp = []
#     if stat == "Missing":
#         bad.append(i[0]-1)
#         continue
#     elif stat == "Graduate":
#         for j in grad_short_qs:
#             resp.append(i[col_conv(j)])
#         for k in list(Counter(resp).items()):
#             if (k[1] > 1 and len(str(k[0])) > 3) or len(str(k[0])) == 1:
#                 bad.append(i[0]-1)
#                 break
#         continue
#     elif stat == "Undergraduate":
#         for j in ug_short_qs:
#             resp.append(i[col_conv(j)])
#         for k in list(Counter(resp).items()):
#             if (k[1] > 1 and len(str(k[0])) > 3) or len(str(k[0])) == 1:
#                 bad.append(i[0]-1)
#                 break
#         continue
#     elif stat == "Both":
#         if completion_time < complete_min*2:
#             bad.append(i[0]-1)
#             continue
#         for j in np.concatenate((grad_short_qs, ug_short_qs)):
#             resp.append(i[col_conv(j)])
#         for k in list(Counter(resp).items()):
#             if (k[1] > 1 and len(str(k[0])) > 3) or len(str(k[0])) == 1:
#                 bad.append(i[0]-1)
#                 break
#         continue

results = np.delete(dat, np.array(bad), 0)
df_results = pd.DataFrame(data=results[0:,1:], index=results[0:,0], columns=np.array(raw_dat.columns)[1:])
df_results.to_excel("output.xlsx")

# TESTS
print(len(results))
print(len(bad))
print(len(results) + len(bad) == len(dat))
