import requests
import json

if __name__ == "__main__":
    # County code to test with
    county_code = 37
    state_code = 19

    # URL of your Flask server
    url = 'http://127.0.0.1:5000/predict'  # Adjust the URL if your server is running on a different port or host

    # Data to send in the request (in JSON format)
    data = {'COUNTY_CODE': county_code,
            'STATE_CODE': state_code}

    # Send a POST request to the server
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Print the predictions returned by the server
        predictions = response.json()['predictions']
        mse = response.json()['mse']
        print(f'Predictions for county code {county_code}: {predictions}')
        print(f'MSE for county code {county_code}: {mse}')
    else:
        # Print an error message if the request failed
        print(f'Error: {response.status_code}')