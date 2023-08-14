# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-23

Script for de-botting Cell & Systems Biology UTQAP survey data.
Written for use by the UofT Innovation Hub.
"""
# Why can't numpy directly read excel files...
import numpy as np
import pandas as pd
import debot_helpers as dh
from collections import Counter
from time import sleep
from sys import exit

# Reassuring message
print("Hello! This may take up to a minute. Please stand by.")

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

# Conditionals, grouped for easy editing
complete_min = 360# Desired completion time minimum in seconds
simple_min = 3# Max length for simple responses (e.g., "no" or "n/a")
grad_short_qs = np.array(["CE","CH"])# Question columns in excel
ug_short_qs = np.array(["CZ","DJ","DS","EJ"])
current = "I"# Column with current student identifier
alum = "L"# Column with alumni identifier
both = "CI"# Column with 'double alumni' identifier

# Identifying bad responses
all_responses = []
# This loop grabs all the short responses in the whole dataset
for i in np.concatenate((grad_short_qs, ug_short_qs)):
    all_responses = np.concatenate((all_responses, dat.T[dh.col_conv(i)]))
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
    stat = dh.student_status(i, current, alum, both, True)
    resp = []
    if stat == "Missing":
        bad.append(i[0]-1)
        continue
    elif stat == "Graduate":
        for j in grad_short_qs:
            resp.append(i[dh.col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue
    elif stat == "Undergraduate":
        for j in ug_short_qs:
            resp.append(i[dh.col_conv(j)])
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
            resp.append(i[dh.col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue

# Results output
results = np.delete(dat, np.array(bad), 0)# Purge bad students from results
rejections = np.delete(dat, np.array([i - 1 for i in list(results.T[0])]), 0)# Rejected data
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