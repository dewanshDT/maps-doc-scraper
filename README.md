# Healthcare Provider Finder

A powerful Python CLI tool that uses Google Maps Places API to find healthcare providers across India. Extract comprehensive information including contact details, ratings, and business hours.

---

## 🚀 Features

- **Flexible Search**: Find any healthcare specialty in any city in India
- **Comprehensive Data**: Extract name, address, phone, website, ratings, opening hours, and more
- **Smart Pagination**: Automatically handles Google's pagination to get maximum results
- **Progress Tracking**: Real-time progress bars and detailed logging
- **Error Handling**: Robust retry logic and graceful error recovery
- **CLI Interface**: Easy-to-use command line interface with multiple options
- **Data Validation**: Validates and cleans extracted data
- **Export to CSV**: Saves results with timestamps for data tracking

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

### Basic Usage

```bash
# Default: Find pediatricians in Mumbai
python main.py

# Search for specific specialty and location
python main.py -q "cardiologists in Delhi"

# Specify output file
python main.py -q "dentists in Bangalore" -o dentists_bangalore.csv

# Limit results
python main.py -q "physiotherapists in Chennai" --max-results 30

# Enable verbose logging
python main.py -q "dermatologists in Kolkata" -v
```

### Command Line Options

```
-q, --query          Search query (default: 'pediatricians in Mumbai')
-o, --output         Output CSV file (default: 'pediatricians_mumbai.csv')
--max-results        Maximum number of results to fetch
-v, --verbose        Enable verbose logging
-h, --help           Show help message
```

### Example Searches

```bash
# Different specialties
python main.py -q "neurologists in Mumbai"
python main.py -q "orthopedic surgeons in Delhi"
python main.py -q "gynecologists in Pune"
python main.py -q "psychiatrists in Hyderabad"

# Different locations
python main.py -q "pediatricians in Chennai"
python main.py -q "cardiologists in Bangalore"
python main.py -q "dentists in Ahmedabad"

# Hospitals and clinics
python main.py -q "hospitals in Mumbai"
python main.py -q "dental clinics in Delhi"
python main.py -q "eye clinics in Bangalore"
```

---

## 📁 Output

The tool generates:

- **CSV file** with all extracted data
- **Log file** (`healthcare_finder.log`) with detailed execution logs
- **Console summary** with statistics

### Sample Output

```
🏥 Healthcare Provider Finder
==================================================
Search Query: cardiologists in Delhi
Output File: cardiologists_delhi.csv
==================================================
INFO - Starting search for: cardiologists in Delhi
INFO - Fetching page 1...
Processing page 1: 100%|████████| 20/20 [00:45<00:00,  2.27s/place]
INFO - Waiting 2s before next page (Google requirement)...
INFO - Search completed. Found 45 providers
✅ Saved 45 results to 'cardiologists_delhi.csv'

📊 Summary:
   • Total providers found: 45
   • Providers with phone numbers: 42
   • Providers with websites: 28
   • Providers with ratings: 38
   • Results saved to: cardiologists_delhi.csv
```

---

## 🔧 Configuration

Edit `config.py` to customize:

- `MAX_RETRIES`: API retry attempts (default: 3)
- `RETRY_DELAY`: Delay between retries (default: 2 seconds)
- `PAGE_TOKEN_DELAY`: Delay between pages (default: 2 seconds)

---

## 📈 Cost Estimation

**API Costs (per search):**

- Text Search: ~$0.017 per request
- Place Details: ~$0.017 per place
- **Total**: ~$0.034 per healthcare provider

**Free Tier:**

- Google provides $200 free credit monthly
- Can process ~5,800 providers per month for free

---

## 🚨 Error Handling

The tool handles various error scenarios:

- **API quota exceeded**: Clear error message with suggestions
- **Invalid API key**: Helpful setup instructions
- **Network timeouts**: Automatic retries with exponential backoff
- **Rate limiting**: Respects Google's rate limits
- **Partial failures**: Continues processing and saves partial results

---

## 🔍 Troubleshooting

### Common Issues:

1. **"Request denied" error**

   - Check if your API key is correct in `.env` file
   - Ensure Places API is enabled in Google Cloud Console

2. **"Quota exceeded" error**

   - Check your Google Cloud billing and quotas
   - Consider upgrading your plan or reducing search scope

3. **No results found**

   - Try broader search terms
   - Check if the location exists in Google Maps
   - Verify your search query spelling

4. **Slow processing**
   - This is normal due to Google's rate limiting
   - Use `--max-results` to limit the number of results

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
