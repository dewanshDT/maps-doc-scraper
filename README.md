# Pediatrician Finder - Mumbai

This Python CLI tool uses the Google Maps Places API to find pediatricians in Mumbai and extract:

- Name
- Address
- Phone Number
- Website
- Tags (Google Place types)

---

## 🚀 Features

- Uses Google Places API to search for pediatricians in Mumbai.
- Fetches up to 60 results per query (API limit).
- Outputs name, address, phone number, website, and Google tags.
- Saves results to `pediatricians_mumbai.csv`.

---

## 🧭 How to Get a Google Maps API Key

1. **Visit Google Cloud Console**  
   https://console.cloud.google.com/

2. **Create a New Project**

   - Click the dropdown on the top-left → “New Project”
   - Name it (e.g., `Pediatrician Finder`) and click **Create**

3. **Enable Billing**

   - Link a credit card (Google gives $200 free usage/month)

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

7. **Paste the Key in `config.py`**
   ```python
   # config.py
   API_KEY = "YOUR_REAL_API_KEY"
   ```
