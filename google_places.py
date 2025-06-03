# google_places.py

import requests
import time
import logging
from config import API_KEY, MAX_RETRIES, RETRY_DELAY

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GooglePlacesError(Exception):
    """Custom exception for Google Places API errors"""
    pass

def make_api_request(url, params, max_retries=MAX_RETRIES):
    """
    Make API request with retry logic and error handling
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Check for Google API specific errors
            if data.get("status") not in ["OK", "ZERO_RESULTS"]:
                error_msg = data.get("error_message", f"API returned status: {data.get('status')}")
                if data.get("status") == "OVER_QUERY_LIMIT":
                    raise GooglePlacesError(f"API quota exceeded: {error_msg}")
                elif data.get("status") == "REQUEST_DENIED":
                    raise GooglePlacesError(f"Request denied - check API key and permissions: {error_msg}")
                else:
                    raise GooglePlacesError(f"API error: {error_msg}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
            else:
                raise GooglePlacesError(f"Failed to make API request after {max_retries} attempts: {e}")
        
        except Exception as e:
            logger.error(f"Unexpected error during API request: {e}")
            raise GooglePlacesError(f"Unexpected error: {e}")

def search_places(query, next_page_token=None):
    """
    Search for places using Google Places Text Search API
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": query,
        "key": API_KEY
    }
    if next_page_token:
        params["pagetoken"] = next_page_token

    logger.info(f"Searching for: {query}")
    return make_api_request(url, params)

def get_place_details(place_id):
    """
    Get detailed information for a specific place
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,types,rating,user_ratings_total,opening_hours,price_level",
        "key": API_KEY
    }
    
    try:
        response = make_api_request(url, params)
        return response.get("result", {})
    except GooglePlacesError as e:
        logger.error(f"Failed to get details for place_id {place_id}: {e}")
        return {}
