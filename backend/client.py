import requests
import json
import time

if __name__ == "__main__":
    # County code to test with
    county_code = 19
    state_code = 47

    # URL of your Flask server
    url = 'http://127.0.0.1:5000/predict'  
    
    # Data to send in the request (in JSON format)
    data = {'COUNTY_CODE': county_code,
            'STATE_CODE': state_code}

    # Retry settings
    max_retries = 3
    retry_delay = 1  # in seconds

    # Send a POST request with retry
    for i in range(max_retries):
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise HTTPError for bad status codes
            break  # Break out of loop if request succeeds
        except requests.exceptions.RequestException as e:
            print(f'Retry {i + 1}: Error encountered - {e}')
            time.sleep(retry_delay)
    else:
        print(f'Failed to connect to server after {max_retries} retries.')
        exit(1)

    # Request was successful, process the response
    if 'next_year_prediction' in response.json():
        next_year_prediction = response.json()['next_year_prediction']
        graph_image_path = response.json()['graph_image']
        print(f'Predicted yield for next year in county {county_code}: {next_year_prediction}')
        print(f'Graph image path: {graph_image_path}')
    else:
        print('No prediction data found in the response.')
