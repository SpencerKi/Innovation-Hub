# Spencer Y. Ki
# 2023-01-19
# Quantify responses to Likert questions and calculate their Pearson correlation coefficients

library(pacman)
p_load(readxl, corrr)

# For my own convenience; sub in your own working directory
setwd("C:/Users/spenc/Desktop/Work/iHub/Analysis")

# Load file data for analysis; replace file as needed
for_analysis <- "ESL (Debotted).xlsx"
raw_dataset <- as.data.frame(read_excel(for_analysis))
dataset <- raw_dataset

# Quantify Likert questions according to regex criteria
dataset <- as.data.frame(lapply(dataset, function(x) gsub("^Not at all.*", 0.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Poor", 0.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Definitely no", 0.0, x)))

dataset <- as.data.frame(lapply(dataset, function(x) gsub("^Slightly.*", 1.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Probably no", 1.0, x)))

dataset <- as.data.frame(lapply(dataset, function(x) gsub("^Moderately.*", 2.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Fair", 2.0, x)))

dataset <- as.data.frame(lapply(dataset, function(x) gsub("^Very.*", 3.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Good", 3.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Probably yes", 3.0, x)))

dataset <- as.data.frame(lapply(dataset, function(x) gsub("^Extremely.*", 4.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Excellent", 4.0, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Definitely yes", 4.0, x)))

dataset <- as.data.frame(lapply(dataset, function(x) gsub("Does not apply", NA, x)))
dataset <- as.data.frame(lapply(dataset, function(x) gsub("Unsure", NA, x)))

# Convert all data to numeric
dataset <- as.data.frame(sapply(dataset, as.numeric))

# Create correlation matrix of variables
correlated <- as.data.frame(cor(dataset, use = "pairwise.complete.obs"))

# Set a minimum correlation threshold to narrow down the presented results; replace number as needed
threshold <- 0.9

# Present only correlations over the threshold; use View() function to print in new window
focus_if(correlated, function(x) any(x >= abs(threshold), na.rm = TRUE), mirror = TRUE)
