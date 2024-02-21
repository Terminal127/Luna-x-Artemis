import requests

def search_wallpapers(query=""):
    # Replace "YOUR_API_KEY" with your actual API key
    api_key = "hzDIqUPXyz50otjd0Sw7xQn31FSHpOFO"
    
    url = f"https://wallhaven.cc/api/v1/search?apikey={api_key}"

    params = {"q": query}
    response = requests.get(url, params=params)
    data = response.json()

    return data

# Example usage
search_results = search_wallpapers(query="anime")
print(search_results)
