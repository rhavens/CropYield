import pandas as pd
import os


# Updated Preprocessing File.
# This function gets called by the backend server.py file to pull only specific county.

def process_county(state_code: int, county_code: int, file_name: str, output_file: str):
    file_path = os.getcwd().replace("backend", "") + os.path.sep + "data" + os.path.sep

    df = pd.read_csv(file_path + file_name)
    only_counties = df.loc[(df['COUNTY_CODE'] == county_code) & (df["STATE_FIPS_CODE"] == state_code)]
    only_counties.to_csv(file_path + output_file, index=False)  # used for debugging
    return only_counties


if __name__ == '__main__':
    process_county(37, 'crop_data_cleaned.csv', 'county_data_subset.csv')
