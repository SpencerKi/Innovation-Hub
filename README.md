# Innovation Hub Repository
Scripts for the Innovation Hub, Division of Student Life, University of Toronto.

## Disclaimer
If anyone not from the iHub is looking at this repository — go away. Yes, the code is bad.

## Using csb_debot.exe (version 1.0 2022-11-17)
0. 64-bit version of Windows required (I'm like 90% sure the office computers fill this requirement).
1. Locate the csb_debot.exe executable in the folder UTQAP > Quantitative Data Analyst > CSB Debotting App in the Sharepoint general files.
2. Download csb_debot.exe to an offline location (it will **not** work in Sharepoint).
3. Spreadsheet of responses downloaded from the MS Forms survey should be copied to the same offline folder as csb_debot.exe. Rename the spreadsheet to "csb.xlsx" but **do not** edit the contents of the spreadsheet.
4. Run csb_debot.exe and follow the instructions on the pop-up window. It may take a minute for instructions to appear. The cleaned CSB responses (cleaned_csb_responses.xlsx) and rejected CSB responses ("rejected_csb_responses.xlsx") should then appear in the folder.

## Using csb_debot.py (version 2.0.1 2022-11-17)
This section is probably only relevant to Tanvi.

0. Python 3.7+ required (Anaconda distribution preferred for the correct packages).
1. Script should be in the same file directory as spreadsheet. Spreadsheet should be renamed "csb.xlsx"
2. Alter parameters to fit desired purging criteria. Alterable parameters detailed below.
3. Run script, cleaned_csb_responses.xlsx and rejected_csb_responses.xlsx should be generated in the active directory.

## Current Purging Criteria
complete_min = 360 <- The expected minimum time to complete the survey in seconds

simple_min = 3 <- The maximum length for a 'simple' response (e.g., "no" or "n/a")

grad_short_qs = ["CE","CH"] <- The Excel columns with the short answer questions for graduate students

ug_short_qs = ["CZ","DJ","DS","EJ"] <- The Excel columns with the short answer questions for undergraduate students

## Current Criteria Priority
1. Is response time under completion minimum? (Logic: The median response time is currently 396 seconds and bots presumably far outnumber real responses)
2. (a) Is the respondent a graduate student?
- If a short answer response is not simple (see criteria above), is it a duplicate? (Logic: removes duplicates that aren't "no", "n/a", or similar)
- Are any short answer responses only a single character long? (Logic: presumably botted responses frequently have single-character responses to short-answer questions)
- Are any short answer questions non-alphanumeric? (Logic: there are a large number of nonsensical responses not in English)
2. (b) Is the respondent an undergraduate student?
- If a short answer response is not simple (see criteria above), is it a duplicate?
- Are any short answer responses only a single character long?
- Are any short answer questions non-alphanumeric?
2. (c) Is the respondent a "both" student?
- Is response time under double the completion minimum? (Logic: "both" students have to respond to both the undergraduate and graduate questions, so double the time is allotted).
- If a short answer response is not simple (see criteria above), is it a duplicate?
- Are any short answer responses only a single character long?
- Are any short answer questions non-alphanumeric?
