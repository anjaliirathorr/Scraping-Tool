from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium options
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass bot detection
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Read URLs from CSV and fetch content
import csv

with open("links.csv", "r") as file:
    reader = csv.reader(file)
    urls = [row[0] for row in reader if row]

for i, url in enumerate(urls):
    try:
        driver.get(url)
        html_content = driver.page_source
        file_path = f"data/page_{i+1}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Saved: {file_path}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

driver.quit()
