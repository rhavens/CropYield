import pandas as pd

# Program for cleaning data in crop yield dataset to prepare it for model predictions
# The program is structured with functions on top, driver code on bottom


# Function to convert all tons values to lbs
def tons_to_lbs(row):

    try:
        if row['UNIT_DESC'] == 'TONS':
            value_in_tons = row['VALUE']
            value_in_tons = value_in_tons.replace(",", "")
            value_in_tons = float(value_in_tons)
            value_in_lbs = value_in_tons * 2000  # 1 ton = 2000 pounds
            preclean.at[row.name, 'UNIT_DESC'] = 'LB'
            return value_in_lbs
        else:
            return row['VALUE']
    except ValueError:
        print(f"Failed to convert '{value_in_tons}' to float")
        return None

# Function to convert bushels to lbs
def bushels_to_lbs(row):
    try:
        if row['UNIT_DESC'] == 'BU':
            value_in_bushels = row['VALUE']
            value_in_bushels = value_in_bushels.replace(",", "")
            value_in_bushels = float(value_in_bushels)

            # 1 bushel = 60 pounds 
            # Info gathered from https://grains.org/markets-tools-data/tools/converting-grain-units/
            value_in_lbs = value_in_bushels * 60  
            preclean.at[row.name, 'UNIT_DESC'] = 'LB'
            return value_in_lbs
        else:
            return row['VALUE']
    except ValueError:
        print(f"Failed to convert '{value_in_bushels}' to float")
        return None



# Driver Code

# Place input file to clean here
preclean = pd.read_csv("data/cropsubset1000.csv")

# Begin Filtering
preclean['VALUE'] = preclean.apply(tons_to_lbs, axis=1)
preclean['VALUE'] = preclean.apply(bushels_to_lbs, axis=1)

preclean.dropna(subset=['VALUE'], inplace=True)
# Check changes
print(preclean.head())

preclean.to_csv('data/testcleandataset.csv', index=False)
