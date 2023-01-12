# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2023-01-11

C O R R E L A T E
"""
import numpy as np
import pandas as pd
import re

title = "cleaned_csb_responses.xlsx"

raw_dat = pd.read_excel(title)
dat = raw_dat.to_numpy()

for i in range(len(dat)):
    for j in range(len(dat.T)):
        if type(dat[i][j]) == str:
            if bool(re.match("^Not at all", dat[i][j])):
                dat[i][j] = 0.0
            elif bool(re.match("^Slightly", dat[i][j])):
                dat[i][j] = 1.0
            elif bool(re.match("^Moderately", dat[i][j])):
                dat[i][j] = 2.0
            elif bool(re.match("^Very", dat[i][j])):
                dat[i][j] = 3.0
            elif bool(re.match("^Extremely", dat[i][j])):
                dat[i][j] = 4.0
            elif bool(re.match("Does not apply", dat[i][j])) or bool(re.match("Unsure", dat[i][j])):
                dat[i][j] = np.nan

valid_qs = []
for i in range(len(dat.T)):
    try:
        dat.T[i].astype(float)
        valid_qs.append(i)
    except:
        continue

threshold = 0.9
correlated = []
for i in range(len(valid_qs)):
    a = np.ma.masked_invalid(dat.T[valid_qs[i]].astype(float))
    for j in range(i+1, len(valid_qs)):
        b = np.ma.masked_invalid(dat.T[valid_qs[j]].astype(float))
        msk = (~a.mask & ~b.mask)
        cor = np.ma.corrcoef(a[msk],b[msk])[0][-1]
        if cor > threshold:
            correlated.append([i, j, cor])