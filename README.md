# Car listings scraper

This tool is used for fetching listings from Autolist based on your chosen brand and amount of pages.

## Installation instructions

```bash
git clone https://github.com/Koste14/car-data-fetching.git
cd car-data-fetching
pip install -r requirements.txt
```

## Usage
Run the following command, where you need to replace BRAND_NAME and NUMBER_OF_PAGES, the --output flag is optional (specified the file location)
```python src/scraper.py --brand BRAND_NAME --pages NUMBER_OF_PAGES --output OUTPUT_FILENAME.xlsx```

