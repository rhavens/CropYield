import pandas as pd

# Updated Preprocessing File. 
# This function gets called by the backend app.py file to pull only specific county.

def process_county(county_code, input_file, output_file):
    
    maindata = input_file
    
    countydata = maindata[maindata['COUNTY_CODE'] == county_code]

    # Save the subset for the specified county to a CSV file
    countydata.to_csv(output_file, index=False)

    print(f"Data subset created for county {county_code}")

if __name__ == '__main__':
    
    process_county('your_county_code', 'main_dataset.csv', 'county_data_subset.csv')
