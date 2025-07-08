import requests
import json
from server.settings import GOOGLE_MAPS_API_KEY

def get_route():
    # Endpoint URL
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    # Request headers with wildcard field mask
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "*"  # Wildcard: request ALL possible fields
    }

    # JSON body with your origin and destination
    body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": 37.740612,
                    "longitude": -121.928033
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": 37.699738,
                    "longitude": -121.928185
                }
            }
        },
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "METRIC"
    }

    # Send the request
    response = requests.post(url, headers=headers, json=body)

    return response
    """
    # Check for success
    if response.status_code == 200:
        print("Route received successfully.")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

    """
