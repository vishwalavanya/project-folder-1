# Technical Assignment Solutions

This repository contains my solutions for the three-part technical assignment covering Python web scraping, SQL queries, and Unix shell scripting.

The assignment contains three separate solutions:

1. Python Web Scraper for MDComputers
2. SQL Queries using the Rfam MySQL Database
3. Unix Shell Script for processing S&P 500 company data

---

## Repository Structure

```text
technical-assignment/
├── README.md
├── scraper.py
├── queries.sql
└── companies.sh
```

Each question is implemented in a separate file inside the main project folder.

| Question | File | Technology |
|----------|------|------------|
| Question 1 | `scraper.py` | Python |
| Question 2 | `queries.sql` | MySQL / SQL |
| Question 3 | `companies.sh` | Bash / Unix Shell |

---

# Question 1 — Python Web Scraper (MDComputers)

**File:** `scraper.py`

## What it does

This Python script searches for products on the MDComputers website and extracts product information from the search results page.

The script retrieves:

- Product name
- Selling price

The user enters a search term, and the program automatically creates the MDComputers search URL, downloads the webpage, parses the HTML, and displays the available products.

## Features

- Accepts a product search term from the user
- Encodes the search term into a valid URL
- Sends an HTTP GET request to MDComputers
- Uses a browser-like User-Agent header
- Parses HTML using BeautifulSoup
- Extracts product names
- Extracts selling prices
- Displays results in a readable format
- Handles empty search terms
- Handles network/request errors
- Handles cases where no products are found

## Prerequisites

The following are required:

- Python 3.6 or higher
- `requests` library
- `beautifulsoup4` library
- Internet connection

## Installation

Install the required Python packages using:

```bash
pip install requests beautifulsoup4
```

## How to Run

Open a terminal in the project folder and run:

```bash
python scraper.py
```

The program will ask for a search term.

For example:

```text
Enter search term: external hard drive
```

The script will then search MDComputers and display the available results.

## Example Output

```text
Fetching results from MDComputers...

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
```

## Error Handling

If the user enters an empty search term:

```text
Error: Search term cannot be empty.
```

If the website cannot be accessed:

```text
Sorry, could not fetch the page. Error: ...
```

If no matching products are found:

```text
No products found for your search term.
Please try a different keyword.
```

## Notes

- Product prices are displayed as they appear on the MDComputers website.
- The results depend on the products currently available on the website.
- The script requires an active internet connection.
- The scraper depends on the HTML structure of the MDComputers website.
- If MDComputers changes its website structure or CSS classes, the HTML selectors may need to be updated.

---

# Question 2 — SQL Queries (Rfam MySQL Database)

**File:** `queries.sql`

## What it does

This file contains SQL queries that retrieve information from the public Rfam MySQL database.

The assignment contains three SQL queries:

- Query A — Count Acacia entries
- Query B — Find the wheat type with the longest DNA sequence
- Query C — Find families with very long DNA sequences and display page 9 of the results

---

## Database Connection Details

| Parameter | Value |
|-----------|-------|
| Host | `mysql-rfam-public.ebi.ac.uk` |
| Port | `4497` |
| User | `rfamro` |
| Password | None |
| Database | `Rfam` |

The database is publicly accessible and is used in read-only mode.

---

## Prerequisites

To execute the SQL queries, a MySQL-compatible client is required.

Examples include:

- MySQL Shell
- MySQL command-line client
- MySQL Workbench
- Other compatible MySQL clients

---

## Connecting Using MySQL Shell

If MySQL Shell is installed, connect using:

```bash
mysqlsh --sql -u rfamro -h mysql-rfam-public.ebi.ac.uk -P 4497
```

If prompted for a password and the public account does not require one, press `Enter`.

After connecting, select the Rfam database:

```sql
USE Rfam;
```

The SQL queries from `queries.sql` can then be executed.

---

## Connecting Using the Traditional MySQL Client

If the traditional `mysql` command-line client is installed, the SQL file can be executed using:

```bash
mysql --user rfamro --host mysql-rfam-public.ebi.ac.uk --port 4497 --database Rfam < queries.sql
```

Individual queries can also be copied and pasted into MySQL Shell, MySQL Workbench, or another compatible client.

---

## Query A — Acacia Types

The first query counts how many entries containing `Acacia` are present in the `taxonomy` table.

```sql
SELECT
    COUNT(*) AS acacia_type_count
FROM taxonomy
WHERE tax_string LIKE '%Acacia%';
```

The query searches the `tax_string` field for taxonomy entries containing the word `Acacia`.

### Example Result

At the time of testing, the query returned:

```text
+-------------------+
| acacia_type_count |
+-------------------+
|               357 |
+-------------------+
```

Database contents can change, so future results may be different.

---

## Query B — Longest Wheat DNA Sequence

The second query finds the wheat type associated with the longest DNA sequence.

It uses:

- `taxonomy`
- `rfamseq`

The tables are joined using the NCBI ID.

```sql
SELECT
    tx.tax_string AS wheat_type,
    rf.length AS dna_sequence_length
FROM taxonomy tx
JOIN rfamseq rf ON tx.ncbi_id = rf.ncbi_id
WHERE tx.tax_string LIKE '%wheat%'
ORDER BY rf.length DESC
LIMIT 1;
```

The query:

1. Searches for wheat-related taxonomy entries.
2. Joins the taxonomy information with sequence information.
3. Sorts the DNA sequence lengths from largest to smallest.
4. Uses `LIMIT 1` to return only the longest sequence.

### Note

Taxonomy databases often use scientific names rather than common English names.

Therefore, depending on the current Rfam data, searching:

```sql
WHERE tx.tax_string LIKE '%wheat%'
```

may return an empty result if the taxonomy uses a scientific name such as `Triticum`.

---

## Query C — Families with Long DNA Sequences (Page 9)

The third query returns:

- Family accession
- Family name
- Maximum DNA sequence length

Only families whose maximum DNA sequence length is greater than `1,000,000` are included.

```sql
SELECT
    f.rfam_acc AS family_accession,
    f.rfam_id AS family_name,
    MAX(rf.length) AS max_dna_sequence_length
FROM family f
JOIN full_region fr ON f.rfam_acc = fr.rfam_acc
JOIN rfamseq rf ON fr.rfamseq_acc = rf.rfamseq_acc
GROUP BY f.rfam_acc, f.rfam_id
HAVING MAX(rf.length) > 1000000
ORDER BY max_dna_sequence_length DESC
LIMIT 15 OFFSET 120;
```

This query joins:

- `family`
- `full_region`
- `rfamseq`

The maximum sequence length is calculated using:

```sql
MAX(rf.length)
```

Only results greater than `1,000,000` are selected using:

```sql
HAVING MAX(rf.length) > 1000000
```

Results are sorted from longest to shortest using:

```sql
ORDER BY max_dna_sequence_length DESC
```

### Pagination

Each page contains 15 results.

Page 9 requires skipping the first 8 pages:

```text
8 × 15 = 120
```

Therefore:

```sql
LIMIT 15 OFFSET 120;
```

returns results 121–135.

---

## Question 2 Notes

- The Rfam public database must be online and accessible.
- An internet connection is required.
- Results depend on the current contents of the Rfam database.
- Some organisms may be stored using scientific taxonomy names rather than common English names.
- The public account has limited database privileges because it is intended for read-only access.

---

# Question 3 — Unix Shell Script (S&P 500 CSV)

**File:** `companies.sh`

## What it does

This Unix shell script downloads an S&P 500 companies CSV file from a URL supplied as a command-line argument.

The script extracts:

- Company name
- Headquarters location
- Founded year

The records are then sorted by founding year from oldest to newest and displayed in a formatted table.

## Features

- Accepts the CSV URL as a command-line argument
- Does not hard-code the dataset URL
- Downloads CSV data using `curl`
- Skips the CSV header
- Extracts required company information
- Extracts a four-digit founding year
- Sorts companies by founding year
- Displays the results in a formatted table
- Handles missing URL arguments
- Handles download failures

---

## Prerequisites

The script requires a Unix/Linux-compatible environment.

Required tools:

- Bash
- `curl`
- `awk`
- `sort`
- `tail`

### Windows Users

On Windows, the script can be executed using:

- Windows Subsystem for Linux (WSL)
- Git Bash
- Another Bash-compatible Unix environment

PowerShell alone does not execute Bash shell scripts in the same way as a Linux/Unix environment.

---

## How to Run

Open a Bash terminal in the project directory.

Give the script execute permission:

```bash
chmod +x companies.sh
```

Run the script and provide the CSV URL:

```bash
./companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
```

The URL is provided as a command-line argument instead of being hard-coded inside the script.

---

## Example Output

```text
========================================================================
Company Name                        Location                  Founded
========================================================================
BNY Mellon                          New York City, New York   1784
...
========================================================================

Done! Results are sorted by founding year (oldest first).
```

---

## Sorting

The script extracts the first four-digit year from the `Founded` field and uses it for sorting.

For example, if the founded value is:

```text
2013 (1888)
```

the first four-digit year:

```text
2013
```

is used as the sorting value.

The final results are sorted numerically from the oldest founding year to the newest.

---

## Error Handling

If the user does not provide a URL:

```text
Error: Please provide the CSV URL as a command-line argument.
Usage: ./companies.sh "DATASET_URL"
```

If the CSV cannot be downloaded:

```text
Error: Failed to retrieve data from the URL.
Please check your internet connection and the URL.
```

---

## Question 3 Notes

- The URL must be provided as a command-line argument.
- The dataset URL is not hard-coded into the script.
- Internet access is required to download the CSV file.
- The script expects a CSV file with the expected S&P 500 dataset column structure.
- Malformed or significantly different CSV data may cause parsing problems.
- The script uses standard Unix command-line utilities for processing and sorting.

---

# Dependencies Summary

| Question | File | Dependencies |
|----------|------|--------------|
| Question 1 | `scraper.py` | Python 3, requests, beautifulsoup4 |
| Question 2 | `queries.sql` | MySQL Shell / MySQL client |
| Question 3 | `companies.sh` | Bash, curl, awk, sort, tail |

---

# How to Run Each Question

## Question 1

Install dependencies:

```bash
pip install requests beautifulsoup4
```

Run:

```bash
python scraper.py
```

---

## Question 2

Connect using MySQL Shell:

```bash
mysqlsh --sql -u rfamro -h mysql-rfam-public.ebi.ac.uk -P 4497
```

Select the database:

```sql
USE Rfam;
```

Then execute the SQL statements available in:

```text
queries.sql
```

---

## Question 3

Using Bash:

```bash
chmod +x companies.sh
```

Then:

```bash
./companies.sh "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv"
```

---

# Assumptions & Limitations

### Question 1

- The MDComputers website is accessible.
- The website's HTML structure is assumed to contain the expected product containers.
- Website redesigns may require changes to the BeautifulSoup selectors.
- Product prices and availability may change over time.

### Question 2

- The Rfam public MySQL database is online and accessible.
- Query results depend on the current database contents.
- Scientific taxonomy names may be used instead of common names.
- A MySQL-compatible client and internet connection are required.

### Question 3

- The supplied URL points to the expected S&P 500 CSV dataset.
- The script requires a Bash-compatible environment.
- Standard Unix utilities such as `curl`, `awk`, `sort`, and `tail` must be available.
- The CSV is expected to have headers and the expected column structure.
- Malformed CSV data or changes to the dataset structure may require modifications to the script.

---

# Technologies Used

- Python
- Requests
- BeautifulSoup
- SQL
- MySQL
- MySQL Shell
- Bash
- curl
- awk
- sort
- tail

---

# Project Files

```text
README.md
scraper.py
queries.sql
companies.sh
```

There are no separate `question1`, `question2`, or `question3` directories. All three solution files are stored directly inside the main project folder.

---

# Conclusion

This technical assignment demonstrates three different approaches to working with external data:

- **Python Web Scraping:** Retrieving and parsing product information from a website.
- **SQL Database Querying:** Retrieving and analyzing biological data from the public Rfam MySQL database.
- **Unix Shell Processing:** Downloading, extracting, sorting, and displaying S&P 500 company information from CSV data.

Each solution is implemented independently and can be executed using the instructions provided above.
