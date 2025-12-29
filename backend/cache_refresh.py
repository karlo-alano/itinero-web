import os, json, requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
APIKEY = os.getenv('GOOGLE_API_KEY')

# Configuration
CATEGORIES = ["restaurant", "cafe", "museum", "park", "church", "tourist_attraction"]
RANKING_TYPES = ["DISTANCE", "POPULARITY"]
CENTER_LOCATION = {"lat": 14.59130, "lng": 120.97505}
MAX_RESULTS = 10
RADIUS = 700.0

# Calculate absolute path to cache file (works regardless of cwd)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE_PATH = os.path.join(SCRIPT_DIR, "..", "database", "storeHours.json")

SEARCH_URL = "https://places.googleapis.com/v1/places:searchNearby"

def initialize_cache_structure():
    """Initialize the empty cache structure"""
    return {
        "last_updated": None,
        "establishments": {}
    }

def fetch_establishments_for_category(category, ranking_type):
    """Fetch top establishments for a specific category and ranking type"""

    params = {
        "includedTypes": [category],
        "maxResultCount": MAX_RESULTS,
        "rankPreference": ranking_type,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": CENTER_LOCATION['lat'],
                    "longitude": CENTER_LOCATION['lng']
                },
                "radius": RADIUS
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": APIKEY,
        "X-Goog-FieldMask": "places.displayName,places.location,places.formattedAddress,places.id,places.regularOpeningHours"
    }

    try:
        print(f"Fetching {ranking_type.lower()} establishments for {category}...")
        response = requests.post(SEARCH_URL, headers=headers, json=params)
        response.raise_for_status()
        data = response.json()

        establishments = []
        for place in data.get('places', []):
            establishment = {
                "place_id": place.get('id'),
                "displayName": place.get('displayName'),
                "location": place.get('location'),
                "formattedAddress": place.get('formattedAddress'),
                "regularOpeningHours": place.get('regularOpeningHours')
            }
            establishments.append(establishment)

        print(f"Found {len(establishments)} establishments")
        return establishments

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {category} with {ranking_type} ranking: {e}")
        return []

def populate_cache():
    """Main function to populate the entire cache"""

    print("Initializing establishments cache...")
    cache_data = initialize_cache_structure()

    # Initialize category structures
    for category in CATEGORIES:
        cache_data["establishments"][category] = {}

    # Fetch data for each category and ranking type
    total_requests = len(CATEGORIES) * len(RANKING_TYPES)
    current_request = 0

    for category in CATEGORIES:
        print(f"\nProcessing category: {category}")

        for ranking_type in RANKING_TYPES:
            current_request += 1
            print(f"Request {current_request}/{total_requests}")

            establishments = fetch_establishments_for_category(category, ranking_type)
            cache_data["establishments"][category][ranking_type.lower()] = establishments

    # Update timestamp (UTC)
    cache_data["last_updated"] = datetime.now(timezone.utc).isoformat()

    # Save to file
    print(f"\nSaving cache to {CACHE_FILE_PATH}...")
    with open(CACHE_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache_data, f, indent=2, ensure_ascii=False)

    print("Cache initialization complete!")
    print(f"Total establishments cached: {sum(len(cat[ranking.lower()]) for cat in cache_data['establishments'].values() for ranking in RANKING_TYPES)}")

if __name__ == "__main__":
    if not APIKEY:
        print("ERROR: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key in a .env file")
        exit(1)

    populate_cache()
