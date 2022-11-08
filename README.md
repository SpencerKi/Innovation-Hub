# Innovation-Hub
Scripts for the Innovation Hub, Division of Student Life, University of Toronto.

## Disclaimer
If anyone not from the iHub is looking at this repository — go away. Yes, the code is bad.

## Using debot.py (version 1.2 2022-11-07)
0. Python 3.7+ required (Anaconda distribution preferred for the correct packages).
1. Script should be in the same file directory as spreadsheet. Spreadsheet should be renamed "qap.xlsx"
2. Alter parameters to fit desired purging criteria. Alterable parameters detailed below.
3. Run script, "output.xlsx" is created in file directory.

## Current Purging Criteria
time_min <- The minimum time in seconds

grad_short_qs <- The Excel columns with the short answer questions for graduate students

ug_short_qs <- The Excel columns with the short answer questions for undergraduate students

## Current Criteria Priority
### Option 1
1. Are any questions responded to?
2. Is response time over 10 minutes?
3. Are short answer responses over 1 character long?

### Option 2
1. Are any questions responded to?
2. Is response time over 6 minutes?
3. (a) Is the respondent a graduate student?
- If a short answer response is identical to another, is the response longer than 3 characters?
- Are any short answer responses only a single character long?
3. (b) Is the respondent an undergraduate student?
- If a short answer response is identical to another, is the response longer than 3 characters?
- Are any short answer responses only a single character long?
3. (c) Is the respondent a "both" student?
- Is response time over 12 minutes?
- If a short answer response is identical to another, is the response longer than 3 characters?
- Are any short answer responses only a single character long?
