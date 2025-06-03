# Multi-Location Healthcare Provider Finder

A powerful Python CLI tool that uses Google Maps Places API to find healthcare providers across multiple locations simultaneously. Extract comprehensive information including contact details, ratings, and business hours from various cities in a single run.

---

## 🚀 Features

- **Multi-Location Search**: Search across multiple cities/locations in a single run
- **Flexible Specialties**: Find any healthcare specialty (doctors, dentists, hospitals, clinics)
- **Comprehensive Data**: Extract name, address, phone, website, ratings, opening hours, and more
- **Smart Pagination**: Automatically handles Google's pagination for maximum results
- **Dual Output Modes**: Combined file or separate files per location
- **Progress Tracking**: Real-time progress bars with location-specific tracking
- **Error Handling**: Robust retry logic and graceful error recovery
- **CLI Interface**: Easy-to-use command line interface with extensive options
- **Data Validation**: Validates and cleans extracted data with location tracking
- **Export to CSV**: Saves results with timestamps and location information

---

## 📊 Extracted Data Fields

- **Name** - Business/provider name
- **Address** - Full formatted address
- **Phone** - Formatted phone number
- **Website** - Business website URL
- **Tags** - Google Place types (e.g., "doctor", "hospital")
- **Rating** - Google rating (1-5 stars)
- **Total Ratings** - Number of reviews
- **Price Level** - Cost indicator (0-4 scale)
- **Opening Hours** - Whether hours are available
- **Search Location** - The city/location searched (optional)
- **Scraped At** - Timestamp of data extraction

---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd maps-doc-scraper
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

---

## 🔑 Getting Google Maps API Key

1. **Visit Google Cloud Console**  
   https://console.cloud.google.com/

2. **Create a New Project**

   - Click the dropdown on the top-left → "New Project"
   - Name it (e.g., `Healthcare Finder`) and click **Create**

3. **Enable Billing**

   - Link a credit card (Google provides $200 free usage monthly)

4. **Enable Required APIs**
   Go to **APIs & Services > Library**, and enable:

   - **Places API**

5. **Create an API Key**

   - Go to **APIs & Services > Credentials**
   - Click **Create Credentials > API Key**
   - Copy the key

6. **Restrict the API Key** (Recommended)

   - Click the key name to edit
   - Under **API restrictions**, select:
     - Restrict to only **Places API**

7. **Add the Key to .env file**
   ```env
   GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

---

## 🎯 Usage

### Basic Multi-Location Usage

```bash
# Use default places from config.py
python main.py

# Override default places with specific locations
python main.py -p "Mumbai,Delhi,Bangalore"

# Multiple locations - semicolon separated
python main.py --places "Chennai; Hyderabad; Kolkata"

# Different specialty using config places
python main.py -s cardiologists

# Different specialty with custom places
python main.py -s cardiologists -p "Mumbai,Delhi,Pune"

# Create separate files for each location
python main.py -s dentists --separate-files

# Limit results per location
python main.py -s physiotherapists --max-per-location 20
```

### Command Line Options

```
-s, --specialty          Healthcare specialty to search for (default: 'pediatricians')
-p, --places             Comma-separated list of places to search (default: places from config.py)
-o, --output             Output CSV file for combined results (default: 'healthcare_providers.csv')
--max-per-location       Maximum number of results per location
--separate-files         Create separate CSV files for each location
--no-location-column     Don't include search location in the data
-v, --verbose            Enable verbose logging
-h, --help               Show help message
```

### Comprehensive Examples

#### Single vs Multiple Locations

```bash
# Single location (traditional approach)
python main.py -s "cardiologists" -p "Mumbai"

# Multiple locations efficiently
python main.py -s "cardiologists" -p "Mumbai,Delhi,Bangalore,Chennai"
```

#### Different Specialties

```bash
# Medical specialists
python main.py -s "neurologists" -p "Mumbai,Delhi,Pune"
python main.py -s "orthopedic surgeons" -p "Bangalore,Chennai"
python main.py -s "gynecologists" -p "Hyderabad,Kolkata"
python main.py -s "psychiatrists" -p "Mumbai,Delhi"

# Dental care
python main.py -s "dentists" -p "Mumbai,Pune,Nashik"
python main.py -s "orthodontists" -p "Delhi,Gurgaon,Noida"

# Healthcare facilities
python main.py -s "hospitals" -p "Mumbai,Delhi,Bangalore"
python main.py -s "diagnostic centers" -p "Chennai,Hyderabad"
python main.py -s "physiotherapy clinics" -p "Pune,Mumbai"
```

#### Output Modes

```bash
# Combined output (default) - all locations in one file
python main.py -s "cardiologists" -p "Mumbai,Delhi" -o cardiologists_multi_city.csv

# Separate files - one file per location
python main.py -s "dentists" -p "Mumbai,Delhi,Bangalore" --separate-files
# Creates: dentists_mumbai.csv, dentists_delhi.csv, dentists_bangalore.csv
```

#### Advanced Usage

```bash
# Limit results and exclude location column
python main.py -s "pediatricians" -p "Mumbai,Delhi" --max-per-location 15 --no-location-column

# Verbose logging for debugging
python main.py -s "dermatologists" -p "Chennai,Bangalore" -v

# Large scale data collection
python main.py -s "general practitioners" -p "Mumbai,Delhi,Bangalore,Chennai,Hyderabad,Kolkata,Pune,Ahmedabad"
```

---

## 📁 Output

The tool generates different outputs based on your configuration:

### Combined Mode (Default)

- **Single CSV file** with all results from all locations
- **Location column** indicating which city each provider was found in
- **Consolidated data** for easy analysis across locations

### Separate Files Mode

- **Individual CSV files** for each location
- **Filename format**: `{specialty}_{location}.csv`
- **Location-specific** data organization

### Additional Files

- **Log file** (`healthcare_finder.log`) with detailed execution logs
- **Console summary** with comprehensive statistics

### Sample Output

```
🏥 Multi-Location Healthcare Provider Finder
============================================================
Specialty: cardiologists
Locations: Mumbai, Delhi, Bangalore
Output Mode: Combined file
Output File: cardiologists_multi_city.csv
============================================================
Processing locations: 100%|████████| 3/3 [02:15<00:00, 45.2s/location]
✅ Saved 127 total results to 'cardiologists_multi_city.csv'

📊 Multi-Location Search Summary:
   • Specialty searched: cardiologists
   • Locations searched: 3
   • Total providers found: 127

📍 Results by Location:
   • Mumbai: 52 providers
   • Delhi: 38 providers
   • Bangalore: 37 providers

📋 Data Quality:
   • Providers with phone numbers: 118
   • Providers with websites: 89
   • Providers with ratings: 103

💾 Output: Combined results saved to 'cardiologists_multi_city.csv'
```

---

## 🔧 Configuration

Edit `config.py` to customize:

- `DEFAULT_SPECIALTY`: Default healthcare specialty
- `DEFAULT_PLACES`: Default list of places to search
- `MAX_RETRIES`: API retry attempts (default: 3)
- `RETRY_DELAY`: Delay between retries (default: 2 seconds)
- `PAGE_TOKEN_DELAY`: Delay between pages (default: 2 seconds)
- `DELAY_BETWEEN_LOCATIONS`: Delay between different locations (default: 1 second)

---

## 📈 Cost Estimation

**API Costs (per location per search):**

- Text Search: ~$0.017 per request
- Place Details: ~$0.017 per place
- **Total**: ~$0.034 per healthcare provider

**Multi-Location Efficiency:**

- **3 cities, 50 providers each**: ~$5.10 total
- **5 cities, 30 providers each**: ~$5.10 total
- **10 cities, 20 providers each**: ~$6.80 total

**Free Tier:**

- Google provides $200 free credit monthly
- Can process ~5,800 providers per month for free
- **Multi-location searches are very cost-effective!**

---

## 🚨 Multi-Location Benefits

### Efficiency Gains

- **Single API key setup** for multiple locations
- **Batch processing** reduces manual work
- **Consolidated logging** for easy monitoring
- **Progress tracking** across all locations

### Data Quality

- **Consistent data structure** across locations
- **Standardized validation** for all results
- **Location tracking** for geographic analysis
- **Timestamp synchronization** across searches

### Analysis Benefits

- **Comparative analysis** between locations
- **Market research** across multiple cities
- **Geographic distribution** insights
- **Scalable data collection** for research

---

## 🔍 Troubleshooting

### Multi-Location Specific Issues:

1. **Slow processing with many locations**

   - This is normal due to API rate limiting
   - Use `--max-per-location` to limit results per city
   - Consider running fewer locations per batch

2. **Some locations return no results**

   - Check location spelling and validity
   - Try broader search terms
   - Verify the location exists in Google Maps

3. **Memory issues with large searches**

   - Use `--separate-files` to reduce memory usage
   - Process fewer locations per run
   - Limit results per location

4. **API quota exceeded**
   - Reduce number of locations per run
   - Use `--max-per-location` to limit results
   - Monitor your Google Cloud usage

### General Issues:

1. **"Request denied" error**

   - Check if your API key is correct in `.env` file
   - Ensure Places API is enabled in Google Cloud Console

2. **No results found**
   - Try broader search terms
   - Verify location spelling
   - Check if the specialty exists in those locations

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📜 License

This project is licensed under the MIT License.

---

## ⚠️ Disclaimer

- Ensure compliance with Google Maps API Terms of Service
- Respect rate limits and usage policies
- The extracted data is for informational purposes only
- Always verify critical information independently
- Multi-location searches may consume API quota faster

---

## ⚙️ Configuration Setup

### Step 1: API Key Setup

Create a `.env` file in the project root:

```env
GOOGLE_MAPS_API_KEY=your_actual_api_key_here
```

### Step 2: Configure Default Places

Edit `config.py` to set your default locations:

```python
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
```

### Step 3: Run the Tool

```bash
# Uses places from config.py by default
python main.py -s "cardiologists"

# Or override with custom places
python main.py -s "cardiologists" -p "Mumbai,Delhi,Pune"
```

---
