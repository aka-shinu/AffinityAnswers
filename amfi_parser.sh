#!/bin/bash

# Download the latest NAV data
curl -s https://www.amfiindia.com/spages/NAVAll.txt -o nav.txt

# Extract Scheme Name ($4) and Net Asset Value ($5), skipping headers and empty lines
awk -F ';' 'BEGIN {OFS="\t"; print "Scheme Name", "Asset Value"} 
    NR > 1 && NF >= 5 && $5 ~ /^[0-9.]+$/ { print $4, $5 }' nav.txt > amfi_data.tsv

echo "✅ Extracted Scheme Name and Asset Value to amfi_data.tsv"
