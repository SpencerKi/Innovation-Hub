# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-23

Script for de-botting general UTQAP survey data. Forked from CSB debotter.
Written for use by the UofT Innovation Hub.
"""
# Why can't numpy directly read excel files...
import numpy as np
import pandas as pd
import debot_helpers as dh
from collections import Counter
from time import sleep
from sys import exit

# Whimsy
print("                  .    |    ,")
print("                   \ _---_ /")
print("                -_ .'     `. _-")
print("               __ :  .---.  : __")
print("                  :  \   /  :")
print("                -' `. | | .' '-")
print("                   / |`-'| \\")
print("                  '  ]'-_[  `")
print("                     ]'-_[")
print("                      '*'")
print("Welcome to the Innovation Hub General Anti-Robot Program!\n")

# Try to load existing configuration settings
configured = False
try:
    # Try loading settings (as dictionary) from a config file if it exists
    settings = dict(
        np.genfromtxt(
            "config.txt", # config.txt will be created at the end of this
            str, 
            delimiter = "=", 
            autostrip = True, 
            skip_header = True)
        )
    # Confirmation that this is the file for analysis...
    loaded = input(
        "\nYour program configuration is set to de-bot " + settings["file_name"] 
        + ".xlsx. Is this correct? [y/n]\n"
        )
    # ...Manual escape if it isn't
    while loaded.lower() != "y" and loaded.lower() != "n":
        loaded = input("\nI'm sorry, that is not a valid response. " + 
                       "Your program configuration is set to de-bot " + 
                       settings["file_name"] + 
                       ".xlsx. Is this correct? [y/n]\n"
                       )
    # Loads pre-set configuration if it is
    if loaded.lower() == "y":
        print("\nThank you! This may take up to a minute. Please stand by.\n")
        file_name = settings["file_name"]
        configured = True
    # Breaks 'try' if it isn't
    elif loaded.lower() == "n":
        raise Exception()
except:
    file_name = input("\nPlease enter the name of the file you need de-botted. " 
      + "Please omit the .xlsx file extension).\n")

try:
    # Data import and conversion to numpy array
    raw_dat = pd.read_excel(file_name + ".xlsx")
    dat = raw_dat.to_numpy()
except:
    # Exception just in case
    print("\nI'm sorry, " + file_name + ".xlsx could not be found. " 
          + "Please ensure the file is named correctly and is in the same " 
          + "file directory as this program. Only .xlsx files will work. " 
          + "Please contact Spencer if problems persist. Thank you!\n")
    sleep(10)
    exit()

# Conditionals, loaded from configuration or manually set
if configured:# As in, if configuration succesfully loaded above
    # Desired completion time minimum in seconds
    complete_min = int(settings["complete_min"])
    # Max length for simple responses (e.g., "no" or "n/a")
    simple_min = int(settings["simple_min"])
    # Graduate question columns in excel
    grad_short_qs = np.array(
        [q.strip() for q in settings["grad_short_qs"].split(",")]
        )
    # Undergraduate question columns in excel
    ug_short_qs = np.array(
        [q.strip() for q in settings["ug_short_qs"].split(",")]
        )
    # Column with current student identifier
    current = settings["current"]
    # Column with alumni identifier
    alum = settings["alum"]
    # Column with 'double alumni' identifier
    both = settings["both"]
else:# If they weren't, enter manually
    complete_min = input("\nWhat is the minimum number of seconds a 'real' " + 
                          "response should take? " + 
                          "Any responses taking less time will be purged.\n")
    simple_min = input("\nWhat is the maximum number of characters a 'simple' " + 
                          "response should take?" + 
                          "Any duplicated responses above that will be purged.\n")
    grad_short_qs = input("\nWhich columns contain short answer questions for " + 
                          "graduate students? Enter the columns seperated " + 
                          "by commas (e.g. I, L, CI). If gradute students " + 
                          "were not a part of this survey, please leave " + 
                          "this question blank.\n")
    ug_short_qs = input("\nWhich columns contain short answer questions for " + 
                          "undergraduate students? Enter the columns seperated " + 
                          "by commas (e.g. I, L, CI). If undergradute students " + 
                          "were not a part of this survey, please leave " + 
                          "this question blank.\n")
    current = input("\nWhich column identifies level of study for current " + 
                    "students? If level of study was not relevant to " + 
                    "this survey (i.e., if only undergraduates or only " + 
                    "graduate students were surveyed), please leave this " + 
                    "question blank.\n")
    alum = input("\nWhich column identifies most recent level of study for " + 
                 "alumni? If alumni were not included in this survey, " + 
                 "or if level of study was not relevant to this survey " + 
                 "(i.e., if only undergraduates or only graduate students " + 
                 " were surveyed), please leave this question blank.\n")
    both = input("\nWhich column identifies current/former graduate students " + 
                 "who also completed their undergraduate studies at UofT? " + 
                 "If graduate students were not a part of this survey, " + 
                 "please leave this question blank.\n")
    
    # Formatting responses
    complete_min = int(complete_min)
    simple_min = int(simple_min)
    if grad_short_qs.strip()  != "":
        grad_short_qs = np.array(
            [q.strip() for q in grad_short_qs.split(",")]
            )
    else:
        grad_short_qs = np.empty(0)
    if ug_short_qs.strip()  != "":
        ug_short_qs = np.array(
            [q.strip() for q in ug_short_qs.split(",")]
            )
    else:
        ug_short_qs = np.empty(0)
    
# Checking if level of study is relevant to the calculations
if current == "" and  alum == "":
    level_relevance = "None"
elif (current != "" or  alum != "") and both == "":
    level_relevance = "Partial"
elif current != "" and  alum != "" and both != "":
    level_relevance = "Total"
else:
    print("\nI'm sorry, something has gone terribly wrong. Please contact Spencer\n")
    sleep(10)
    exit()

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
    
    resp = []
    # Loop if only one level of study was consulted
    if level_relevance == "None":
        # See annotations starting on line 195 for explanation
        if completion_time < complete_min:
            bad.append(i[0]-1)
            continue
        for j in np.concatenate((grad_short_qs, ug_short_qs)):
            resp.append(i[dh.col_conv(j)])
        for k in list(Counter(resp).items()):
            if k[0] in bad_responses:
                bad.append(i[0]-1)
                break
        continue
    # Loop if two levels of study were consulted...
    elif level_relevance == "Partial" or level_relevance == "Total":
        # ...and 'both' was not considered
        if level_relevance == "Partial":
            stat = dh.student_status(i, current, alum, both, False)
        elif level_relevance == "Total":
            stat = dh.student_status(i, current, alum, both, True)
        # if conditions check for student status
        # First for loop in each condition checks which questions should be checked
        # Second for loop checks if any responses are on the bad list
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

# Results printing
df_results.to_excel("cleaned_" + file_name + "_responses.xlsx")
df_rejections.to_excel("rejected_" + file_name + "_responses.xlsx")
# Configuration saving
np.savetxt("config.txt", [
    "HELLO! INSTRUCTIONS ON MANUALLY EDITING THIS FILE ARE ON MY GITHUB.",
    "file_name = " + file_name,
    "complete_min = " + str(complete_min),
    "simple_min = " + str(simple_min),
    "grad_short_qs = " + str(', '.join(list(grad_short_qs))),
    "ug_short_qs = " + str(', '.join(list(ug_short_qs))),
    "current = " + current,
    "alum = " + alum, 
    "both = " + both], fmt = "%s")

# Goodbye!
print("\nCleaned and rejected outputs are now in the file directory! " 
      + "Your program configuration has also been saved for future convenience. " 
      + "Thank you for being awesome, and have a pleasant day!\n")
sleep(10)
exit()