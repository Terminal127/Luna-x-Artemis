import requests

def call_api():
    url = "https://api.screenshotone.com/take?access_key=kWaLGnuRQrDW0g&url=https%3A%2F%2Fkiit.ac.in%2F&full_page=false&viewport_width=1920&viewport_height=1280&device_scale_factor=1&format=jpg&image_quality=80&block_ads=true&block_cookie_banners=true&block_banners_by_heuristics=false&block_trackers=true&delay=0&timeout=60"
    params = None
    method = "GET"
    headers = None
    data = None
    response = requests.request(method, url, headers=headers, params=params, data=data)
    print ("response code: ", response.status_code)
    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")