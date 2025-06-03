#!/usr/bin/env python3
"""
Healthcare Provider Finder

A CLI tool to find healthcare providers using Google Maps Places API.
Supports different specialties and locations.
"""

import argparse
import time
import csv
import logging
import sys
from datetime import datetime
from tqdm import tqdm
from config import DEFAULT_SEARCH_QUERY, DEFAULT_OUTPUT_FILE, PAGE_TOKEN_DELAY
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

class HealthcareProviderFinder:
    def __init__(self, search_query, output_file, max_results=None):
        self.search_query = search_query
        self.output_file = output_file
        self.max_results = max_results
        self.results = []
        
    def validate_place_data(self, details):
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
        
        # Basic validation
        if validated_data["name"] == "N/A":
            logger.warning("Place found with no name - skipping")
            return None
            
        return validated_data
    
    def fetch_providers(self):
        """
        Fetch healthcare providers with progress tracking
        """
        logger.info(f"Starting search for: {self.search_query}")
        page_token = None
        page_count = 0
        
        try:
            while True:
                page_count += 1
                logger.info(f"Fetching page {page_count}...")
                
                # Search for places
                data = search_places(self.search_query, next_page_token=page_token)
                places = data.get("results", [])
                
                if not places:
                    logger.info("No more results found")
                    break
                
                # Process each place with progress bar
                with tqdm(places, desc=f"Processing page {page_count}", unit="place") as pbar:
                    for place in pbar:
                        if self.max_results and len(self.results) >= self.max_results:
                            logger.info(f"Reached maximum results limit: {self.max_results}")
                            return self.results
                        
                        try:
                            details = get_place_details(place["place_id"])
                            validated_data = self.validate_place_data(details)
                            
                            if validated_data:
                                self.results.append(validated_data)
                                pbar.set_postfix({"Found": len(self.results)})
                            
                        except Exception as e:
                            logger.error(f"Error processing place {place.get('name', 'Unknown')}: {e}")
                            continue
                
                # Check for next page
                page_token = data.get("next_page_token")
                if page_token:
                    logger.info(f"Waiting {PAGE_TOKEN_DELAY}s before next page (Google requirement)...")
                    time.sleep(PAGE_TOKEN_DELAY)
                else:
                    break
                    
        except GooglePlacesError as e:
            logger.error(f"Google Places API error: {e}")
            if not self.results:
                raise
        except KeyboardInterrupt:
            logger.info("Search interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            if not self.results:
                raise
        
        logger.info(f"Search completed. Found {len(self.results)} providers")
        return self.results
    
    def save_to_csv(self):
        """
        Save results to CSV with error handling
        """
        if not self.results:
            logger.warning("No results to save")
            return False
        
        try:
            with open(self.output_file, "w", newline="", encoding="utf-8") as f:
                fieldnames = self.results[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
            
            logger.info(f"✅ Saved {len(self.results)} results to '{self.output_file}'")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save CSV file: {e}")
            return False
    
    def print_summary(self):
        """
        Print a summary of the results
        """
        if not self.results:
            print("No results found.")
            return
        
        print(f"\n📊 Summary:")
        print(f"   • Total providers found: {len(self.results)}")
        print(f"   • Providers with phone numbers: {sum(1 for r in self.results if r['phone'] != 'N/A')}")
        print(f"   • Providers with websites: {sum(1 for r in self.results if r['website'] != 'N/A')}")
        print(f"   • Providers with ratings: {sum(1 for r in self.results if r['rating'] != 'N/A')}")
        print(f"   • Results saved to: {self.output_file}\n")

def create_parser():
    """
    Create command line argument parser
    """
    parser = argparse.ArgumentParser(
        description="Find healthcare providers using Google Maps Places API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Default: pediatricians in Mumbai
  python main.py -q "cardiologists in Delhi"       # Cardiologists in Delhi
  python main.py -q "dentists in Bangalore" -o dentists.csv
  python main.py -q "physiotherapists in Chennai" --max-results 30
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        default=DEFAULT_SEARCH_QUERY,
        help=f"Search query (default: '{DEFAULT_SEARCH_QUERY}')"
    )
    
    parser.add_argument(
        "-o", "--output",
        default=DEFAULT_OUTPUT_FILE,
        help=f"Output CSV file (default: '{DEFAULT_OUTPUT_FILE}')"
    )
    
    parser.add_argument(
        "--max-results",
        type=int,
        help="Maximum number of results to fetch (default: no limit)"
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
    
    # Display startup info
    print("🏥 Healthcare Provider Finder")
    print("=" * 50)
    print(f"Search Query: {args.query}")
    print(f"Output File: {args.output}")
    if args.max_results:
        print(f"Max Results: {args.max_results}")
    print("=" * 50)
    
    try:
        # Create finder instance
        finder = HealthcareProviderFinder(
            search_query=args.query,
            output_file=args.output,
            max_results=args.max_results
        )
        
        # Fetch providers
        results = finder.fetch_providers()
        
        if results:
            # Save to CSV
            if finder.save_to_csv():
                finder.print_summary()
            else:
                logger.error("Failed to save results")
                sys.exit(1)
        else:
            print("❌ No results found. Try a different search query.")
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
