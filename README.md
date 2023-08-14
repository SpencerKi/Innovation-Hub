# Innovation Hub Repository
Scripts for the Innovation Hub, Division of Student Life, University of Toronto. Primarily written for the UTQAP team, but survey-related scripts should be generalisable to any survey. I don't work there anymore, but I'm always happy to help and am only an email away!

## Analysis
If everyone absolutely insists on using Microsoft Forms for data collection, the scripts in the Analysis folder can clean their ridiculous output and return useful sample statistics and visualisations. I exported .exes of these but no one was using them and we needed space on the Sharepoint so only scripts are left. Instructions are as follows:

### Using utqap_analysis.py
likert_quantifier.R is the functional equivalent of this script in R, if preferred.

0. Python 3.7+ required (Anaconda distribution preferred for the correct packages).
1. Lines 40-46 should have the corresponding columns in the raw Excel output filled in.
2. Lines 12-20 are customised user prompts for the 2022-2023 data; I recommend commenting them out and replacing the values in Lines 22-36 directly.
3. Everything should go smoothly from there.

### Using likert_visualiser.py
This script has functionally the same format as utqap_analysis.py, but outputs useful Likert plots for the comms team to play with.

## Debotting
During the 2022–2023 UTQAP survey process, we got hit by hundreds of obviously fake respondents presumably looking for a gift card. Hopefully this isn't relevant in the future, but the below code was our ad hoc solution to figuring out which responses were real and which were fake. The settings are determined by the config.txt in the Debotting folder. Instructions are as follows:

### Using debot.exe (version 1.0 2022-11-23)
0. 64-bit version of Windows required (I'm like 90% sure the office computers fill this requirement).
1. Locate the debot.exe executable in the folder UTQAP > Quantitative Data Analyst > Debotting App in the Sharepoint general files.
2. Download debot.exe to an offline location (it will **not** work in Sharepoint).
3. Download the spreadsheet of responses from the MS Forms survey and copy them to the same offline folder as debot.exe. **Do not** edit the columns or column headers of the spreadsheet (editing individual responses ahead of time is fine, if you need to).
4. Run debot.exe and follow the instructions on the pop-up window. It may take a minute for instructions to appear. The cleaned responses (cleaned\_[PROJECT NAME]\_responses.xlsx) and rejected responses ("rejected\_[PROJECT NAME]\_responses.xlsx") should then appear in the folder.
5. A configuration file should also be outputted, to speed up the process next time you use the app - it saves the input settings from the most recent program run. The values in this config file can be edited manually as long as you don't touch anything to the left side of the equals sign.

**Most troubleshooting is covered in the "Current Purging Criteria" section below. Otherwise, ask me if something completely unusual goes wrong!**

### Using debot.py (version 1.0 2022-11-23)
0. Python 3.7+ required (Anaconda distribution preferred for the correct packages).
1. Both scripts (*debot.py* and *debot_helpers.py*) should be in the same file directory as spreadsheet. You shouldn't really need to open *debot_helpers.py*, it's just there to hold helper functions.
2. Alter parameters to fit desired purging criteria. Nearly all *print()* and *input()* lines are only there for the executable and can be safely deleted/commented out if working with the script directly. For one, you can skip the entire try/except ridiculousness from lines 31-64. Additionally, the if/else conditions on lines 80 and 99 are based on user input; remove lines 80 and 99-129, unindenting 81-98. Alternatively, see step 3 (b) below.
3. (a) The rest of that should run as a fairly straightforward script, but if things are needlessly messy it might be easier to just run the deprecated csb_debot.py script below.
3. (b) Alternatively, if the script is working but its just annoying to repeatedly fiddle with the conditionals, keep the input/print and try/except lines where they are and just write a config file manually. An example one for the CSB survey is included in this repository - feel free to edit the variable values but do not edit the variable names.

### Current Purging Criteria / config.txt Settings
file_name <- The name of the spreadsheet file excluding ".xlsx". If encountering difficulty at this stage, make sure that the spreadsheet file is in the correct directory, the spreadsheet file is name correctly, and that the spreadsheet is actually in .xlsx form (and not, for example, a .csv).

complete_min <- The expected minimum time to complete the survey in seconds. This must be an int value (i.e., a whole number). Any responses with responses times under this value will be purged.

simple_min <- The maximum length for a 'simple' response (e.g., "no" or "n/a"). If a short answer is a duplicate and *not* a simple response, it will be purged.

grad_short_qs <- The Excel columns with the short answer questions for graduate students. This condition exists to check for duplicates, so if a column with multiple choice responses is entered here, *a lot* of duplicates will be detected. Can be omitted if graduate students were not included in the survey (if editing the config.txt file, just leave the variable value blank but keep the variable).

ug_short_qs <- The Excel columns with the short answer questions for undergraduate students. This condition exists to check for duplicates, so if a column with multiple choice responses is entered here, *a lot* of duplicates will be detected. Can be omitted if undergraduate students were not included in the survey (if editing the config.txt file, just leave the variable value blank but keep the variable).

current <- The Excel column with the question checking for level of study for current students (i.e., are they currently graduate students or undergraduates?). Do *not* enter the question asking for year of study here. Can be omitted if only one level of study was considered (i.e., only undergraduates or only graduates - if editing the config.txt file, just leave the variable value blank but keep the variable).

alum <- The Excel column with the question checkingfor most recent level of study for alumni (i.e., were they graduate students or undergraduates?). Can be omitted if only one level of study was considered (i.e., only undergraduates or only graduates) or if alumni were not consulted (if editing the config.txt file, just leave the variable value blank but keep the variable).

both <- The Excel column with the question checking whether current/alumni graduate students were also formerly undergraduates students (i.e., did they also do their undergrad in the same department?). Can be omitted if this question was not asked (if editing the config.txt file, just leave the variable value blank but keep the variable).

**Edge cases have custom error messages written by me. The only way to throw up some sort of system error is from an incorrect setting reading - please let me know if that happens and I'll troubleshoot manually.**

### Current Criteria Priority (in the CSB Example)
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
