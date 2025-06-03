#!/usr/bin/env python3
"""
Healthcare Provider Finder

A CLI tool to find healthcare providers using Google Maps Places API.
Supports different specialties across multiple locations simultaneously.
"""

import argparse
import time
import csv
import logging
import sys
import os
from datetime import datetime
from tqdm import tqdm
from config import (
    DEFAULT_SPECIALTY, DEFAULT_PLACES, DEFAULT_OUTPUT_FILE, 
    PAGE_TOKEN_DELAY, DELAY_BETWEEN_LOCATIONS,
    DEFAULT_SEPARATE_FILES, DEFAULT_INCLUDE_LOCATION_IN_DATA
)
from google_places import search_places, get_place_details, GooglePlacesError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('healthcare_finder.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MultiLocationHealthcareFinder:
    def __init__(self, specialty, places, output_file, max_results_per_location=None, 
                 separate_files=False, include_location_in_data=True):
        self.specialty = specialty
        self.places = places if isinstance(places, list) else [places]
        self.output_file = output_file
        self.max_results_per_location = max_results_per_location
        self.separate_files = separate_files
        self.include_location_in_data = include_location_in_data
        self.all_results = []
        self.results_by_location = {}
        
    def create_search_query(self, specialty, place):
        """
        Create search query for specific specialty and place
        """
        return f"{specialty} in {place}"
        
    def validate_place_data(self, details, location=None):
        """
        Validate and clean place data
        """
        validated_data = {
            "name": details.get("name", "N/A"),
            "address": details.get("formatted_address", "N/A"),
            "phone": details.get("formatted_phone_number", "N/A"),
            "website": details.get("website", "N/A"),
            "tags": ", ".join(details.get("types", [])),
            "rating": details.get("rating", "N/A"),
            "total_ratings": details.get("user_ratings_total", "N/A"),
            "price_level": details.get("price_level", "N/A"),
            "opening_hours": "Available" if details.get("opening_hours") else "N/A",
            "scraped_at": datetime.now().isoformat()
        }
        
        # Add location information if requested
        if self.include_location_in_data and location:
            validated_data["search_location"] = location
        
        # Basic validation
        if validated_data["name"] == "N/A":
            logger.warning("Place found with no name - skipping")
            return None
            
        return validated_data
    
    def fetch_providers_for_location(self, location):
        """
        Fetch healthcare providers for a specific location
        """
        search_query = self.create_search_query(self.specialty, location)
        logger.info(f"Searching for: {search_query}")
        
        location_results = []
        page_token = None
        page_count = 0
        
        try:
            while True:
                page_count += 1
                logger.info(f"Fetching page {page_count} for {location}...")
                
                # Search for places
                data = search_places(search_query, next_page_token=page_token)
                places = data.get("results", [])
                
                if not places:
                    logger.info(f"No more results found for {location}")
                    break
                
                # Process each place with progress bar
                desc = f"Processing {location} (Page {page_count})"
                with tqdm(places, desc=desc, unit="place", leave=False) as pbar:
                    for place in pbar:
                        if (self.max_results_per_location and 
                            len(location_results) >= self.max_results_per_location):
                            logger.info(f"Reached max results limit for {location}: {self.max_results_per_location}")
                            return location_results
                        
                        try:
                            details = get_place_details(place["place_id"])
                            validated_data = self.validate_place_data(details, location)
                            
                            if validated_data:
                                location_results.append(validated_data)
                                pbar.set_postfix({"Found": len(location_results)})
                            
                        except Exception as e:
                            logger.error(f"Error processing place {place.get('name', 'Unknown')}: {e}")
                            continue
                
                # Check for next page
                page_token = data.get("next_page_token")
                if page_token:
                    logger.debug(f"Waiting {PAGE_TOKEN_DELAY}s before next page for {location}...")
                    time.sleep(PAGE_TOKEN_DELAY)
                else:
                    break
                    
        except GooglePlacesError as e:
            logger.error(f"Google Places API error for {location}: {e}")
            if not location_results:
                raise
        except KeyboardInterrupt:
            logger.info(f"Search interrupted by user for {location}")
        except Exception as e:
            logger.error(f"Unexpected error during search for {location}: {e}")
            if not location_results:
                raise
        
        logger.info(f"Completed search for {location}. Found {len(location_results)} providers")
        return location_results
    
    def fetch_all_providers(self):
        """
        Fetch healthcare providers for all locations
        """
        logger.info(f"Starting multi-location search for {self.specialty}")
        logger.info(f"Locations: {', '.join(self.places)}")
        
        total_locations = len(self.places)
        
        # Main progress bar for locations
        with tqdm(self.places, desc="Processing locations", unit="location") as location_pbar:
            for i, location in enumerate(location_pbar):
                location_pbar.set_description(f"Processing {location}")
                
                try:
                    # Fetch providers for this location
                    location_results = self.fetch_providers_for_location(location)
                    
                    if location_results:
                        self.results_by_location[location] = location_results
                        self.all_results.extend(location_results)
                        
                        location_pbar.set_postfix({
                            "This location": len(location_results),
                            "Total found": len(self.all_results)
                        })
                    else:
                        logger.warning(f"No results found for {location}")
                    
                    # Delay between locations to be respectful to the API
                    if i < total_locations - 1:  # Don't delay after the last location
                        time.sleep(DELAY_BETWEEN_LOCATIONS)
                        
                except Exception as e:
                    logger.error(f"Failed to process {location}: {e}")
                    continue
        
        logger.info(f"Multi-location search completed. Total providers found: {len(self.all_results)}")
        return self.all_results
    
    def save_results(self):
        """
        Save results to CSV file(s)
        """
        if not self.all_results:
            logger.warning("No results to save")
            return False
        
        success = True
        
        try:
            if self.separate_files:
                # Save separate file for each location
                for location, results in self.results_by_location.items():
                    if not results:
                        continue
                    
                    # Create filename based on location and specialty
                    safe_location = location.lower().replace(" ", "_").replace(",", "")
                    safe_specialty = self.specialty.lower().replace(" ", "_")
                    filename = f"{safe_specialty}_{safe_location}.csv"
                    
                    self._save_csv_file(results, filename)
                    logger.info(f"✅ Saved {len(results)} results for {location} to '{filename}'")
            else:
                # Save all results to single file
                self._save_csv_file(self.all_results, self.output_file)
                logger.info(f"✅ Saved {len(self.all_results)} total results to '{self.output_file}'")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            success = False
        
        return success
    
    def _save_csv_file(self, results, filename):
        """
        Helper method to save results to a specific CSV file
        """
        with open(filename, "w", newline="", encoding="utf-8") as f:
            if results:
                fieldnames = results[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(results)
    
    def print_summary(self):
        """
        Print a comprehensive summary of the results
        """
        if not self.all_results:
            print("No results found.")
            return
        
        print(f"\n📊 Multi-Location Search Summary:")
        print(f"   • Specialty searched: {self.specialty}")
        print(f"   • Locations searched: {len(self.places)}")
        print(f"   • Total providers found: {len(self.all_results)}")
        
        # Summary by location
        print(f"\n📍 Results by Location:")
        for location, results in self.results_by_location.items():
            count = len(results) if results else 0
            print(f"   • {location}: {count} providers")
        
        # Data quality summary
        phone_count = sum(1 for r in self.all_results if r.get('phone', 'N/A') != 'N/A')
        website_count = sum(1 for r in self.all_results if r.get('website', 'N/A') != 'N/A')
        rating_count = sum(1 for r in self.all_results if r.get('rating', 'N/A') != 'N/A')
        
        print(f"\n📋 Data Quality:")
        print(f"   • Providers with phone numbers: {phone_count}")
        print(f"   • Providers with websites: {website_count}")
        print(f"   • Providers with ratings: {rating_count}")
        
        # File output info
        if self.separate_files:
            print(f"\n💾 Output: Separate files created for each location")
        else:
            print(f"\n💾 Output: Combined results saved to '{self.output_file}'")
        print()

def parse_places_argument(places_str):
    """
    Parse places argument which can be comma-separated or semicolon-separated
    If places_str is None, returns DEFAULT_PLACES from config
    """
    if places_str is None:
        return DEFAULT_PLACES
    
    # Split by comma or semicolon and clean up
    if ',' in places_str:
        places = [place.strip() for place in places_str.split(',')]
    elif ';' in places_str:
        places = [place.strip() for place in places_str.split(';')]
    else:
        places = [places_str.strip()]
    
    # Filter out empty strings
    places = [place for place in places if place]
    
    return places if places else DEFAULT_PLACES

def create_parser():
    """
    Create command line argument parser
    """
    parser = argparse.ArgumentParser(
        description="Find healthcare providers across multiple locations using Google Maps Places API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use places from config.py (default)
  python main.py

  # Override with specific locations
  python main.py -p "Mumbai,Delhi,Bangalore"
  python main.py --places "Chennai; Hyderabad; Kolkata"
  
  # Different specialty with config places
  python main.py -s cardiologists
  
  # Different specialty with custom places
  python main.py -s cardiologists -p "Mumbai,Delhi,Pune"
  
  # Separate files for each location
  python main.py -s dentists --separate-files
  
  # Limit results per location
  python main.py -s physiotherapists --max-per-location 20
        """
    )
    
    parser.add_argument(
        "-s", "--specialty",
        default=DEFAULT_SPECIALTY,
        help=f"Healthcare specialty to search for (default: '{DEFAULT_SPECIALTY}')"
    )
    
    parser.add_argument(
        "-p", "--places",
        default=None,  # Make it None so we can detect if user provided it
        help=f"Comma-separated list of places to search (default: config file places: {', '.join(DEFAULT_PLACES)})"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output CSV file for combined results (default: '{DEFAULT_OUTPUT_FILE}')"
    )
    
    parser.add_argument(
        "--max-per-location",
        type=int,
        help="Maximum number of results per location (default: no limit)"
    )
    
    parser.add_argument(
        "--separate-files",
        action="store_true",
        help="Create separate CSV files for each location"
    )
    
    parser.add_argument(
        "--no-location-column",
        action="store_true",
        help="Don't include search location in the data"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    return parser

def main():
    """
    Main function
    """
    parser = create_parser()
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Parse places
    places = parse_places_argument(args.places)
    
    # Display startup info
    print("🏥 Multi-Location Healthcare Provider Finder")
    print("=" * 60)
    print(f"Specialty: {args.specialty}")
    print(f"Locations: {', '.join(places)}")
    print(f"Output Mode: {'Separate files' if args.separate_files else 'Combined file'}")
    if not args.separate_files:
        print(f"Output File: {args.output}")
    if args.max_per_location:
        print(f"Max Results per Location: {args.max_per_location}")
    print("=" * 60)
    
    try:
        # Create finder instance
        finder = MultiLocationHealthcareFinder(
            specialty=args.specialty,
            places=places,
            output_file=args.output,
            max_results_per_location=args.max_per_location,
            separate_files=args.separate_files,
            include_location_in_data=not args.no_location_column
        )
        
        # Fetch providers
        results = finder.fetch_all_providers()
        
        if results:
            # Save results
            if finder.save_results():
                finder.print_summary()
            else:
                logger.error("Failed to save results")
                sys.exit(1)
        else:
            print("❌ No results found across all locations. Try different search terms.")
            sys.exit(1)
            
    except GooglePlacesError as e:
        logger.error(f"Google Places API error: {e}")
        print("\n💡 Tips:")
        print("   • Check your API key in the .env file")
        print("   • Ensure Places API is enabled in Google Cloud Console")
        print("   • Verify you have sufficient API quota")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
