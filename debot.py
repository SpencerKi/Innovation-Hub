# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-17

Script for de-botting Cell & Systems Biology UTQAP survey data.
Written for use by the UofT Innovation Hub.
"""
# Reassuring message for the executable
print("Hello! This may take up to a minute. Please stand by.")

# Why can't numpy directly read excel files...
import numpy as np
import pandas as pd
from collections import Counter
from time import sleep
from sys import exit

try:
    # Data import and conversion to numpy array
    raw_dat = pd.read_excel("csb.xlsx")
    dat = raw_dat.to_numpy()
except:
    # Exception just in case
    print("I'm sorry, csb.xlsx could not be found. " 
          + "Please ensure the excel file is named 'csb' and is in the same " 
          + "file directory as this program. Only .xlsx files will work. " 
          + "Please contact Spencer if problems persist. Thank you!")
    sleep(10)
    exit()

# Assorted helper functions that really should be in a module
def col_conv(col: str) -> float:
    """Converts excel column to usable indices.
    col: Alphabetic column identifier (e.g., "A" for the first column)
    return: Python-usable index
    
    >>> col_conv("A")
    0
    >>> col_conv("AB")
    27
    """
    num = 0
    for c in col:
        num = num * 26 + (ord(c.upper()) - ord('A')) + 1# Based on Unicode IDs
    return num - 1

def student_status(student: np.ndarray) -> str:
    """Checks if a student responded to the grad and/or undergrad questions.
    student: Array of a respondent's answers to the survey
    return: String indicating student status
    
    Test cases vary by data.
    """
    # Questions I and L ask for level of study for current students and alumni
    if isinstance(student[col_conv("I")], str) \
    or isinstance(student[col_conv("L")], str):
        if student[col_conv("I")] == "Graduate" \
        or student[col_conv("L")] == "Graduate":
            # Question CI asks if they also completed undergrad at UofT
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

def fetch_stats(df: pd.DataFrame, q: str) -> pd.core.series.Series:
    """Gives statistical overview of responses to one question.
    df: DataFrame of results (e.g., uncleaned dat or cleaned df_results)
    q: Alphabetic column identifier for the desired question
    
    This is here for diagnostic and is unused by the main script.
    """
    return df.iloc()[:,col_conv(q)].describe()

# Conditionals, grouped for easy editing
complete_min = 360# Desired completion time minimum in seconds
simple_min = 3# Max length for simple responses (e.g., "no" or "n/a")
grad_short_qs = np.array(["CE","CH"])# Question columns in excel
ug_short_qs = np.array(["CZ","DJ","DS","EJ"])

# Identifying bad responses
all_responses = []
# This loop grabs all the short responses in the whole dataset
for i in np.concatenate((grad_short_qs, ug_short_qs)):
    all_responses = np.concatenate((all_responses, dat.T[col_conv(i)]))
bad_responses = []
# This loop identifies which of the responses are undesirable
# - First condition removes duplicates over specified length
# - Second removes single character responses
# - Third removes non-alphanumerics
for i in list(Counter(all_responses).items()):
    if (i[1] > 1 and len(str(i[0])) > simple_min) \
    or len(str(i[0])) == 1 \
    or not all(ord(c) < 128 for c in str(i[0])):
        bad_responses.append(i[0])

# This for loop checks all students in the dataset one-by-one
bad = []# Stores index of bad students
for i in dat:   
    # i[2] and i[1] are end and start time
    completion_time = (i[2]-i[1]).total_seconds()

    # Check for desired minimum completion time
    if completion_time < complete_min:
        bad.append(i[0]-1)
        continue
    
    # if conditions check for student status
    # First for loop in each condition checks which questions should be checked
    # Second for loop checks if any responses are on the bad list
    stat = student_status(i)
    resp = []
    if stat == "Missing":
        bad.append(i[0]-1)
        continue
    elif stat == "Graduate":
        for j in grad_short_qs:
            resp.append(i[col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue
    elif stat == "Undergraduate":
        for j in ug_short_qs:
            resp.append(i[col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue
    elif stat == "Both":
        if completion_time < complete_min*2:
            bad.append(i[0]-1)
            continue
        for j in np.concatenate((grad_short_qs, ug_short_qs)):
            resp.append(i[col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue

# Results output
results = np.delete(dat, np.array(bad), 0)# Purge bad students from results
rejections = np.delete(dat, np.array(list(results.T[0])), 0)# Rejected data
# Conversion to DataFrame
df_results = pd.DataFrame(
    data=results[0:,1:], 
    index=results[0:,0], 
    columns=np.array(raw_dat.columns)[1:])
df_rejections = pd.DataFrame(
    data=rejections[0:,1:], 
    index=rejections[0:,0], 
    columns=np.array(raw_dat.columns)[1:])
# Output
df_results.to_excel("cleaned_csb_responses.xlsx")
df_rejections.to_excel("rejected_csb_responses.xlsx")

# Goodbye!
print("Cleaned and rejected outputs are now in the file directory! " 
      + "Thank you for being awesome, and have a pleasant day!")
sleep(10)
exit()
