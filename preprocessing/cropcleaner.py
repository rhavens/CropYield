import pandas as pd

# Program for cleaning data in crop yield dataset to prepare it for model predictions
# The program is structured with functions on top, driver code on bottom


# Driver Code

# Place input file to clean here
preclean = pd.read_csv("data/cropsubset1000.csv")

# Eliminate anything before GMO (1994). 
# Source: https://www.fda.gov/food/agricultural-biotechnology/science-and-history-gmos-and-other-food-modification-processes
preclean = preclean[preclean['YEAR'] >= 1994]

preclean['VALUE'] = preclean['VALUE'].apply(lambda x: None if x == '(D)' else x)
preclean.dropna(subset=['VALUE'], inplace=True)

preclean = preclean[preclean['UNIT_DESC'].isin(['BU'])]
columns_to_drop = ['SECTOR_DESC', 'GROUP_DESC', 'DOMAINCAT_DESC', 'SHORT_DESC', 'STATISTICCAT_DESC', 'PRODN_PRACTICE_DESC', 'GROUP_DESC', 'SECTOR_DESC', 'REFERENCE_PERIOD_DESC', 'LOCATION_DESC', 'ASD_CODE', 'ASD_DESC', 'UTIL_PRACTICE_DESC']
preclean.drop(columns_to_drop, axis=1, inplace=True)

preclean = preclean[preclean['SOURCE_DESC'] != 'SURVEY']


# Check changes
print(preclean.head())

preclean.to_csv('modeldata.csv', index=False)
