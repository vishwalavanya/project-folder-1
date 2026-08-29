#!/bin/bash

# ============================================================
# S&P 500 Companies CSV Processor
# Usage: ./companies.sh "DATASET_URL"
# ============================================================

# I am creating this check to make sure the user provides a URL
if [ $# -eq 0 ]; then
    echo "Error: Please provide the CSV URL as a command-line argument."
    echo "Usage: $0 \"DATASET_URL\""
    exit 1
fi

# I am creating this variable to store the provided CSV URL
CSV_URL="$1"

# I am downloading the CSV data from the given URL
echo "Downloading CSV data from the provided URL..."
CSV_DATA=$(curl -sL "$CSV_URL" 2>/dev/null)

# I am creating this check to make sure the download was successful
if [ -z "$CSV_DATA" ]; then
    echo "Error: Failed to retrieve data from the URL."
    echo "Please check your internet connection and the URL."
    exit 1
fi

echo "Data downloaded successfully."
echo ""

# I am creating the header for the output table
echo "========================================================================"
printf "%-35s %-25s %-15s\n" "Company Name" "Location" "Founded"
echo "========================================================================"

# I am processing, sorting, and formatting the CSV data
echo "$CSV_DATA" | tail -n +2 | awk -F',' '
{
    company = $2
    location = $5
    founded = $8

    # I am creating a fallback for missing founded values
    if (founded == "" || founded ~ /^[[:space:]]*$/) {
        founded = $NF
    }

    # I am removing surrounding quotes from the fields
    gsub(/^"|"$/, "", company)
    gsub(/^"|"$/, "", location)
    gsub(/^"|"$/, "", founded)

    # I am extracting the first four-digit year for sorting
    if (match(founded, /[0-9]{4}/)) {
        sort_year = substr(founded, RSTART, 4)
    } else {
        sort_year = "0000"
    }

    print sort_year "\t" company "\t" location "\t" founded
}
' | sort -t$'\t' -k1,1n | awk -F'\t' '
{
    printf "%-35s %-25s %-15s\n", $2, $3, $4
}
'

# I am creating the footer to show that processing is complete
echo "========================================================================"
echo ""
echo "Done! Results are sorted by founding year (oldest first)."