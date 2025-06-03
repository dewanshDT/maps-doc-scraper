# google_places.py

import requests
from config import API_KEY

def search_places(query, next_page_token=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY
    }
    if next_page_token:
        params["pagetoken"] = next_page_token

    response = requests.get(url, params=params)
    return response.json()

def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,types",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("result", {})
