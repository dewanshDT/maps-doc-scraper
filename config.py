# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Maps API Configuration
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY")

# Default search configurations
DEFAULT_SPECIALTY = "pediatricians"
DEFAULT_OUTPUT_FILE = "healthcare_providers.csv"

# Places to search (modify this list as needed)
DEFAULT_PLACES = [
    "Mumbai",
    "Delhi", 
    "Bangalore",
    "Chennai",
    "Hyderabad",
    "Kolkata",
    "Pune",
    "Ahmedabad"
]

# Multi-location configurations
DEFAULT_SEPARATE_FILES = False  # Whether to create separate files for each location
DEFAULT_INCLUDE_LOCATION_IN_DATA = True  # Whether to add location column to data

# API Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
PAGE_TOKEN_DELAY = 2  # seconds (required by Google)
DELAY_BETWEEN_LOCATIONS = 1  # seconds between different location searches

# Validate API key
if API_KEY == "YOUR_GOOGLE_MAPS_API_KEY" or not API_KEY:
    print("⚠️  Warning: Please set your GOOGLE_MAPS_API_KEY in a .env file or environment variable")
    print("   Create a .env file with: GOOGLE_MAPS_API_KEY=your_actual_api_key")
