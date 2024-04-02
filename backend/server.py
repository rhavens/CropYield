import os
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import data_filterer
from flask import Flask, send_from_directory



app = Flask(__name__)
CORS(app)

# Define the directory to save static files
STATIC_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.config['STATIC_FOLDER'] = STATIC_FOLDER

def generate_plot(X, y, next_year, next_year_prediction):
    plt.figure(figsize=(10, 6))
    plt.scatter(X, y, color='blue', label='Historical Yield')
    plt.scatter(next_year, next_year_prediction, color='red', label='Predicted Yield for Next Year')
    plt.xlabel('Year')
    plt.ylabel('Yield')
    plt.title('Crop Yield Over Years')
    plt.legend()
    plt.grid(True)
    temp_file = os.path.join(app.config['STATIC_FOLDER'], 'temp_plot.png')
    plt.savefig(temp_file)
    plt.close()  # Close plot to prevent memory leaks
    return temp_file

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    county_code = data.get('COUNTY_CODE')
    state_code = data.get('STATE_CODE')
    if county_code is None:
        return jsonify({'error': 'Missing COUNTY_CODE in request data'}), 400
    if state_code is None:
        return jsonify({'error': 'Missing STATE_CODE in request data'}), 400

    input_file = 'crop_data_cleaned.csv'  # Adjust the input file path as needed
    output_file = f'state_{state_code}_county_{county_code}_subset.csv'  # Adjust the output file path as needed

    county_data = data_filterer.process_county(state_code, county_code, input_file, output_file)
    # county_data = pd.read_csv(output_file)

    X = county_data[['YEAR']]
    y = county_data[["VALUE"]]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    current_year = datetime.now().year
    next_year = current_year + 1
    next_year_data = pd.DataFrame({'YEAR': [next_year]})
    next_year_prediction = model.predict(next_year_data)

    generate_plot(X, y, next_year, next_year_prediction)

    # Prepare results
    results = {
        'nextYearPrediction': next_year_prediction.tolist()[0],  # Assuming single prediction
        'graph_image': 'http://127.0.0.1:5000/static/temp_plot.png'
    }

    return jsonify(results)

# Define a route to serve static files
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
