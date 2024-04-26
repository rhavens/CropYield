import pandas as pd
import os


# Updated Preprocessing File.
# This function gets called by the backend server.py file to pull only specific county.
# State code of -1 means select all states
# County code of -1 means select all counties in that state
def process_county(state_code: int, county_code: int, file_name: str, output_file: str):
    file_path = os.getcwd().replace("backend", "") + os.path.sep + "data" + os.path.sep

    df = pd.read_csv(file_path + file_name)
    df = df.loc[df["COUNTY_CODE"] != 998]   # County Aggregate, should not be included
    df = df.loc[df["YEAR"] >= 2000]   # County Aggregate, should not be included
    result = None
    if state_code == -1:
        country_data = {"YEAR": [],
                        "VALUE": []}
        for year in range(1900, 2024):
            year_value = df.loc[df['YEAR'] == year, 'VALUE'].sum()
            if year_value > 0:
                country_data["YEAR"].append(year)
                country_data["VALUE"].append(year_value)

        result = pd.DataFrame(country_data)
    elif county_code == -1:
        result = df.loc[df["STATE_FIPS_CODE"] == state_code]
        state_data = {"YEAR": [],
                        "VALUE": []}
        for year in range(1900, 2024):
            year_value = result.loc[result['YEAR'] == year, 'VALUE'].sum()
            if year_value > 0:
                state_data["YEAR"].append(year)
                state_data["VALUE"].append(year_value)

        result = pd.DataFrame(state_data)
    else:
        result = df.loc[(df['COUNTY_CODE'] == county_code) & (df["STATE_FIPS_CODE"] == state_code)]
    # only_counties = df.loc[(df['county_code'] == county_code) & (df["state_code"] == state_code)]

    result.to_csv(file_path + output_file, index=False)  # used for debugging
    return result


if __name__ == '__main__':
    state_code = -1
    county_code = -1
    input_file = 'crop_data_cleaned.csv'  # Adjust the input file path as needed
    output_file = f'state_{state_code}_county_{county_code}_subset.csv'  # Adjust the output file path as needed

    process_county(state_code, county_code, input_file, output_file)
