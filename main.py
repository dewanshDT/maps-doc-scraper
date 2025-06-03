# main.py

import time
import csv
from config import SEARCH_QUERY
from google_places import search_places, get_place_details

def fetch_pediatricians():
    all_results = []
    page_token = None

    while True:
        data = search_places(SEARCH_QUERY, next_page_token=page_token)
        for place in data.get("results", []):
            details = get_place_details(place["place_id"])
            all_results.append({
                "name": details.get("name"),
                "address": details.get("formatted_address"),
                "phone": details.get("formatted_phone_number"),
                "website": details.get("website"),
                "tags": ", ".join(details.get("types", []))
            })

        page_token = data.get("next_page_token")
        if page_token:
            time.sleep(2)  # Google requires a short wait before using next_page_token
        else:
            break

    return all_results

def save_to_csv(results, filename="pediatricians_mumbai.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    print("Fetching data...")
    results = fetch_pediatricians()
    save_to_csv(results)
    print(f"Saved {len(results)} results to 'pediatricians_mumbai.csv'")
