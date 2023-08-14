# -*- coding: utf-8 -*-
"""
Spencer Y. Ki
2022-11-23

Module of helper functions for de-botting general UTQAP survey data.
Forked from CSB debotter. Written for use by the UofT Innovation Hub.
"""
import numpy as np
import pandas as pd

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

def student_status(student: np.ndarray, current: str, alum: str, both: str,
                   both_relevance: bool) -> str:
    """Checks if a student responded to the grad and/or undergrad questions.
    student: Array of a respondent's answers to the survey
    current: String of excel column with current student identifier question
    alum: String of excel column with alumni identifier question
    both: String of excel column identifying 'double alumni'
    both_relevance: Bool whether 'both' question is relevant
    return: String indicating student status
    
    Test cases vary by data.
    """
    # Questions 'current' and 'alum' ask for level of study for current
    # students and alumni respectively
    if isinstance(student[col_conv(current)], str) \
    or isinstance(student[col_conv(alum)], str):
        if student[col_conv(current)] == "Graduate" \
        or student[col_conv(alum)] == "Graduate":
            # Question 'both' asks if they also completed undergrad at UofT
            if both_relevance:    
                if student[col_conv(both)] == "Yes":
                    return "Both"
                elif student[col_conv(both)] == "No":
                    return "Graduate"
                else:
                    return "Missing"
            else:
                return "Graduate"
        elif student[col_conv(current)] == "Undergraduate" \
        or student[col_conv(alum)] == "Undergraduate":
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