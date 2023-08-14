# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2023-02-16

Script for correcting de-botting UTQAP survey data.
Written for use by the UofT Innovation Hub.
"""
import numpy as np
import pandas as pd

project = "csb"

original = f"{project}.xlsx"
debotted = f"cleaned_{project}_responses.xlsx"
corrections = f"{project}_exceptions.xlsx"
output = f"{project}_retention_results.xlsx"

# Data import and conversion to numpy array
raw_orig = pd.read_excel(original)
orig = raw_orig.to_numpy()

raw_debot = pd.read_excel(debotted)
debot = raw_debot.to_numpy()

re = [string.replace(u'\xa0', u'') for string in pd.read_excel(corrections).to_numpy().flatten().astype(str)]
re = [string for string in re if len(string) > 5]

unneeded = list(orig.T[0])
for i in orig:
    for j in re:
        if j in i:
            if not i[0] in list(debot.T[0]):
                unneeded.remove(i[0])
                break
    continue

unneeded = np.array(unneeded) - 1

# Results output
results = np.delete(orig, unneeded, 0)# Purge bad students from results
# Conversion to DataFrame
df_results = pd.DataFrame(
    data=results[0:,1:], 
    index=results[0:,0], 
    columns=np.array(raw_orig.columns)[1:])
# Output
df_results.to_excel(output)