import requests
from app.config.settings import GOOGLE_MAPS_API_KEY


def get_route_data(origin, destination, mode):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data