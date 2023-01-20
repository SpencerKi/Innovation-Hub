# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2023-01-19

Quantify responses to Likert questions and calculate their Pearson correlation coefficients
"""
import numpy as np
import pandas as pd
import re

# Load file data for analysis; replace file as needed
title = "ESL (Debotted).xlsx"
raw_dat = pd.read_excel(title)
dat = raw_dat.to_numpy()

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
            elif bool(re.search("Does not apply", dat[i][j])) \
                or bool(re.match("Unsure", dat[i][j])):
                dat[i][j] = np.nan

# Separate question columns with valid datatypes for correlation
valid_qs = []
for i in range(len(dat.T)):
    try:
        dat.T[i].astype(float)
        valid_qs.append(i)
    except:
        continue


# Set a minimum correlation threshold to narrow down the presented results; replace number as needed
threshold = 0.8

# Create 'correlation matrix' of variables that correlate over the threshold
correlated = []
for i in range(len(valid_qs)):
    a = np.ma.masked_invalid(dat.T[valid_qs[i]].astype(float))
    for j in range(i+1, len(valid_qs)):
        b = np.ma.masked_invalid(dat.T[valid_qs[j]].astype(float))
        msk = (~a.mask & ~b.mask)
        cor = np.ma.corrcoef(a[msk],b[msk])[0][-1]
        # Commenting out next line results in 'true' correlation matrix
        # Strangely, missing 6786 - 6670 = 116 correlations otherwise [FIX]
        if np.abs(cor) >= threshold:
            correlated.append([raw_dat.columns[valid_qs[i]], 
                               raw_dat.columns[valid_qs[j]], 
                               cor])

# Present sorted correlations (try len() and np.shape() functions as well)
print(correlated)
