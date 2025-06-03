# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google Maps API Configuration
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "YOUR_GOOGLE_MAPS_API_KEY")

# Default search configurations
DEFAULT_SEARCH_QUERY = "pediatricians in Mumbai"
DEFAULT_OUTPUT_FILE = "pediatricians_mumbai.csv"

# API Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
PAGE_TOKEN_DELAY = 2  # seconds (required by Google)

# Validate API key
if API_KEY == "YOUR_GOOGLE_MAPS_API_KEY" or not API_KEY:
    print("⚠️  Warning: Please set your GOOGLE_MAPS_API_KEY in a .env file or environment variable")
    print("   Create a .env file with: GOOGLE_MAPS_API_KEY=your_actual_api_key")
