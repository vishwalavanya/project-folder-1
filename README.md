Technical Assignment Solutions
This repository contains my solutions for the three-part technical assignment covering Python web scraping, SQL queries, and Unix shell scripting.
Repository Structure
plain

project folder/
├── README.md
├── question1/
│   └── scraper.py
├── question2/
│   └── queries.sql
└── question3/
    └── companies.sh

Question 1 — Python Web Scraper (MDComputers)
File: question1/scraper.py
What it does
This script searches for products on the MDComputers website and extracts the product name and selling price from the search results page.
Prerequisites

    Python 3.6 or higher
    requests library
    beautifulsoup4 library

Installation
bash

pip install requests beautifulsoup4

How to run
bash

cd question1
python scraper.py

Then type your search term when prompted, for example:
plain

Enter search term: external hard drive

Example Output
plain

============================================================
Search Results for: external hard drive
============================================================
Total products found: 12
------------------------------------------------------------
1. Seagate Expansion 1TB External Hard Drive
   Price: ₹8,899

2. Western Digital Elements 1TB External Hard Drive
   Price: ₹8,980
...

Notes

    The script handles empty search terms and network errors.
    If no products are found, a friendly message is displayed.
    Prices are shown exactly as they appear on the website.

Question 2 — SQL Queries (Rfam MySQL Database)
File: question2/queries.sql
Database Connection Details
Table
Parameter	Value
Host	mysql-rfam-public.ebi.ac.uk
Port	4497
User	rfamro
Password	none
Database	Rfam
How to run
Connect using any MySQL client, for example:
bash

mysql --user rfamro --host mysql-rfam-public.ebi.ac.uk --port 4497 --database Rfam < question2/queries.sql

Or copy-paste individual queries into MySQL Workbench / command line.
Query A — Acacia Types
Counts how many Acacia plant entries exist in the taxonomy table by matching tax_string.
Query B — Longest Wheat DNA
Finds the wheat type with the longest DNA sequence by joining taxonomy and rfamseq tables, sorting by sequence length in descending order.
Query C — Families with Long DNA (Page 9)
Returns family accession, name, and maximum DNA sequence length for families where the max length is greater than 1,000,000. Results are sorted descending and paginated to show page 9 (rows 121–135).
Question 3 — Unix Shell Script (S&P 500 CSV)
File: question3/companies.sh
What it does
This script downloads an S&P 500 CSV file from a given URL, extracts company name, headquarters location, and founding year, then sorts and displays the records by founding year.
Prerequisites

    Unix/Linux environment or WSL on Windows
    curl installed
    Standard utilities: awk, sort, tail

How to run
bash

cd question3
chmod +x companies.sh
./companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"

Example Output
plain

========================================================================
Company Name                        Location                  Founded
========================================================================
BNY Mellon                          New York City, New York   1784
...
========================================================================
Done! Results are sorted by founding year (oldest first).

Notes

    The URL must be passed as a command-line argument (not hard-coded).
    The script handles missing arguments and download failures.
    For founding years with complex formats like 2013 (1888), the first 4-digit year is used for sorting.

Dependencies Summary
Table
Question	Dependencies
Q1	Python 3, requests, beautifulsoup4
Q2	MySQL client (any)
Q3	bash, curl, awk, sort
Assumptions & Limitations

    Q1: The HTML structure of MDComputers is assumed to use div.product-layout containers. If the site redesigns, selectors may need updating.
    Q2: The Rfam public database must be online and accessible. Query results depend on the current database state.
    Q3: The CSV is expected to have headers and comma-separated values with standard quoting. Malformed CSV may cause parsing issues.