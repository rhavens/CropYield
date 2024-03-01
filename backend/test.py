import requests
import json

# County code to test with
county_code = 37

# URL of your Flask server
url = 'http://127.0.0.1:5000/predict'  # Adjust the URL if your server is running on a different port or host

# Data to send in the request (in JSON format)
data = {'countyCode': county_code}

# Send a POST request to the server
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Print the predictions returned by the server
    predictions = response.json()['predictions']
    print(f'Predictions for county code {county_code}: {predictions}')
else:
    # Print an error message if the request failed
    print(f'Error: {response.status_code}')