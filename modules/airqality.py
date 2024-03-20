# uses aqi api
import requests
import json

# Replace 'YOUR_API_KEY' with your actual API key
api_key = ''

url = 'https://airquality.googleapis.com/v1/currentConditions:lookup?key=' + api_key

# JSON data to be sent in the POST request
data = {
    "universalAqi": True,
    "location": {
        "latitude": 20.3555462,
        "longitude": 85.7980762
    },
    "extraComputations": [
        "HEALTH_RECOMMENDATIONS",
        "DOMINANT_POLLUTANT_CONCENTRATION",
        "POLLUTANT_CONCENTRATION",
        "LOCAL_AQI",
        "POLLUTANT_ADDITIONAL_INFO"
    ],
    "languageCode": "en"
}

# Headers for the request
headers = {'Content-Type': 'application/json'}

# Perform the POST request
response = requests.post(url, json=data, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Request successful!")

    # Pretty print the JSON response
    formatted_response = json.dumps(response.json(), indent=2)
    print(formatted_response)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
