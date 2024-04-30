import os
import pandas as pd
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime
import data_filterer

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def predict():
    data = request.get_json()
    county_code = data.get('COUNTY_CODE')
    state_code = data.get('STATE_CODE')
    if county_code is None:
        return jsonify({'error': 'Missing COUNTY_CODE in request data'}), 400
    if state_code is None:
        return jsonify({'error': 'Missing STATE_CODE in request data'}), 400

    input_file = 'crop_data_cleaned_pruned_v2.csv'  # Adjust the input file path as needed
    output_file = f'state_{state_code}_county_{county_code}_subset.csv'  # Adjust the output file path as needed

    county_data = data_filterer.process_county(state_code, county_code, input_file, output_file)

    # X = county_data[['YEAR']]
    # y = county_data[["VALUE"]]
    X = county_data[['year']]
    y = county_data[['value']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    current_year = datetime.now().year
    next_year = current_year + 1
    # next_year_data = pd.DataFrame({'YEAR': [next_year]})
    next_year_data = pd.DataFrame({'year': [next_year]})
    next_year_prediction = model.predict(next_year_data)

    # Prepare results
    results = {
        'nextYearPrediction': next_year_prediction.tolist()[0],  # Assuming single prediction
        'cleaned_csv_data': county_data.to_dict(orient='records')
    }

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
