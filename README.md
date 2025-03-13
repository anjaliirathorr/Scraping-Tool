# Scrapping-Tool

Overview

This Scraping Tool is designed to extract data from websites without relying on third-party APIs, reducing dependencies and providing greater flexibility. It allows users to scrape, process, and extract relevant data efficiently.

Features

Removes dependency on third-party APIs

Automates data extraction from web pages

Allows customization of scraping parameters

Processes raw HTML to extract required data

Installation & Usage

Prerequisites

Python installed on your system (if not installed, download from Python.org)

Steps to Run the Tool

Extract the files into an empty folder.

Install Python if not already installed.

Open Command Prompt.

Navigate to the extracted folder using: 

cd path/to/extracted-folder  

Create a folder named data inside the extracted folder:

mkdir data  

If needed, update starting URL, start page, and end page in the .env file.

Run the scraping script:

python getdata.py  

Once the above script finishes running, execute:

python gethtml.py  

After running the above command, process the extracted data with:

python process.py  

Contribution & Support

Feel free to contribute or report any issues by raising a ticket in the repository.
