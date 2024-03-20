# uses places api new 

import requests

# Replace 'YOUR_API_KEY' with your actual API key
api_key = ''

url = 'https://places.googleapis.com/v1/places:searchNearby'

# JSON data to be sent in the POST request
data = {
    "includedTypes": ["restaurant"],
    "maxResultCount": 10,
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 20.3555462,
                "longitude": 85.7980762
            },
            "radius": 3000.0
        }
    }
}

# Headers for the request
headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': 'places.displayName'  # Specify the fields you want in the response
}

# Perform the POST request
response = requests.post(url, json=data, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Request successful!")

    # Print the response in a readable format
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
