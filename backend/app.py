from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import cropcleaner  # Import your preprocessing script

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    
    data = request.get_json()
    county_code = data['countyCode']
    input_file = 'data/crop_data_cleaned.csv'  
    output_file = f'data/county_{county_code}_subset.csv' 
    cropcleaner.process_county(county_code, input_file, output_file)
    county_data = pd.read_csv(output_file)

    # Load 
    X = county_data[['YEAR', 'VALUE']]
    y = county_data['CropYield']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions using the trained model
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)

    results = {
        'predictions': predictions.tolist(), 
        'mse': mse
    }
    print(results)
    # return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
