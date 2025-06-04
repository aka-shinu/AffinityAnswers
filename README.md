# AffinityAnswers Data Extraction Scripts

This repository contains two independent scripts for web data extraction, useful for data engineering and analytics tasks.

---

## 1. OLX Car Cover Scraper (`olx_scraper.py`)

A Python script that scrapes car cover listings from OLX India using Selenium and undetected-chromedriver.

**Features:**
- Handles infinite scroll and the "Load More" button to collect all available listings.
- Extracts the following details for each listing:
  - Title
  - Price
  - Location
  - Date
  - Link
  - Image URL
- Saves the results to a CSV file: `olx_car_cover.csv`.

**Usage:**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script:
   ```bash
   python olx_scraper.py
   ```
3. The output will be saved as `olx_car_cover.csv` in the current directory.

**CSV Output Example:**
| Title | Price | Location | Date | Link | Image |
|-------|-------|----------|------|------|-------|
| Car cover-Swift dezire zxi | ₹ 1,300 | CHANNASANDRA SAI LOTUS, BENGALURU | TODAY | https://www.olx.in/item/... | ... |

---

## 2. AMFI NAV Parser (`amfi_parser.sh`)

A Bash script to download and parse the latest NAV (Net Asset Value) data from the AMFI India website.

**Features:**
- Downloads the latest NAV data as `nav.txt`.
- Extracts the scheme name and asset value using `awk`.
- Outputs the results to `amfi_data.tsv`.

**Usage:**
```bash
bash amfi_parser.sh
```
The output will be saved as `amfi_data.tsv` in the current directory.

---

## Requirements

- Python 3.7+
- Google Chrome browser (for Selenium)
- Bash shell (for the AMFI parser)
- The following Python packages (see `requirements.txt`):
  - requests
  - beautifulsoup4
  - undetected-chromedriver>=3.5.0
  - selenium>=4.10.0

Install Python dependencies with:
```bash
pip install -r requirements.txt
```

---

## License

MIT License

---

## Contact

For questions or contributions, please contact the repository owner.
