import requests
import subprocess
import os
from PIL import Image

def getmap(query, zoomlevel):
    api_key = ""  # Replace with your Google Maps API key

    url = "https://maps.googleapis.com/maps/api/staticmap?"
    center = query
    zoom = zoomlevel
    size = "1280x720"
    api_url = f"{url}center={center}&zoom={zoom}&size={size}&key={api_key}&sensor=false"

    response = requests.get(api_url)

    if response.status_code == 200:
        print("Request successful!")
        # Save the map image with a specific path
        map_image_path = os.path.join(os.getcwd(), 'C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna\\apisgoogle\\map_image.png')
        with open(map_image_path, 'wb') as f:
            f.write(response.content)
        return map_image_path
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)
        return None

def open_photo():
    image = Image.open("C:\\Users\\KIIT\\Desktop\\courses\\ai\\luna\\apisgoogle\\map_image.png")
    image.show()

if __name__ == "__main__":
    map = input("Enter the location: ")
    getmap(map, 10)
    open_photo()
