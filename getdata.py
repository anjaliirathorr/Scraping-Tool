import os
import csv
import json
import time
import requests
from dotenv import load_dotenv
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Ensure data directory exists
if not os.path.exists("data"):
    os.makedirs("data")

# Load existing links from CSV
try:
    with open('links.csv', 'rt') as fin:
        cin = csv.reader(fin)
        links = set(row[0] for row in cin)  # Use a set to prevent duplicates
except:
    links = set()

baseurl = os.getenv('BASE_URL')
start_page = int(os.getenv('START_PAGE'))
end_page = int(os.getenv('END_PAGE'))

# Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
chrome_options.add_argument("--disable-gpu")  # Fix ffmpeg errors
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--mute-audio")  # Prevent background media
chrome_options.add_argument("--disable-extensions")  # Block unnecessary extensions
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Speed up loading
chrome_options.add_argument("--disable-remote-fonts")  # Prevent external font issues
chrome_options.add_argument("--ignore-certificate-errors")  # Fix SSL error
chrome_options.add_argument("--allow-running-insecure-content")  # Allow non-HTTPS content
chrome_options.add_argument("--disable-features=InterestCohort")  # Block ad tracking
chrome_options.add_argument("--no-sandbox")  # Allow running in environments like Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent crashes in some environments

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

for pg in range(start_page, end_page + 1):
    page_url = f"{baseurl}page={pg}"

    # Only add pagination link if not already in the set
    if page_url not in links:
        links.add(page_url)

    driver.get(page_url)
    time.sleep(3)  # Allow JavaScript to load

    # Get HTML after JS execution
    response = Selector(text=driver.page_source)

    # Extract JSON data from script tags
    script_texts = response.css('script[type="application/json"]::text').getall()

    for script in script_texts:
        try:
            json_data = json.loads(script)  # Parse JSON data

            def extract_urls(data):
                """ Recursively extract URLs from JSON """
                if isinstance(data, dict):
                    for key, value in data.items():
                        if key == "url" and isinstance(value, str):
                            url = value.strip()
                            if url.startswith("/") and not url.startswith("//"):
                                url = "https://uae.dubizzle.com" + url
                            if url.startswith("http") and url not in links:
                                # Only add relevant listing URLs, avoiding duplicate pagination
                                if "/property-for-sale/residential/apartment/" in url or \
                                   "/property-for-sale/residential/" in url and "sorting=verified_listing_desc" in url:
                                    links.add(url)
                        extract_urls(value)
                elif isinstance(data, list):
                    for item in data:
                        extract_urls(item)

            extract_urls(json_data)

        except json.JSONDecodeError:
            continue

    # Extract property listing links from page
    listing_links = response.css('a[href*="/property-for-sale/residential/apartment/"]::attr(href)').getall()
    for link in listing_links:
        full_url = "https://uae.dubizzle.com" + link if link.startswith("/") else link
        links.add(full_url)

# Close Selenium WebDriver
driver.quit()

# Remove duplicate links, normalize `/en/` versions, and sort them
normalized_links = {link.replace('/en/', '/') for link in links}  # Remove language variations

# Save to CSV
with open('links.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for url in sorted(normalized_links):
        writer.writerow([url])

print("Extracted Unique Links:", sorted(normalized_links))
