import pandas as pd

# Program for cleaning data in crop yield dataset to prepare it for model predictions
# The program is structured with functions on top, driver code on bottom


# Function to convert all tons values to lbs
def tons_to_lbs(row):

    try:
        if row['UNIT_DESC'] == 'TONS':
            value_in_tons = float(row['VALUE'])
            value_in_lbs = value_in_tons * 2000  # 1 ton = 2000 pounds
            return value_in_lbs
        else:
            return row['VALUE']
    except ValueError:
        return None








# Driver Code

# Place input file to clean here
preclean = pd.read_csv("data/CropYieldSubset.csv")


# Begin Filtering
preclean['VALUE'] = preclean.apply(tons_to_lbs, axis=1)

# Apply the conversion function to the 'BU / ACRE' column
print(preclean.head())

