# ST-PHPScrape

This repository contains a simple Python script to collect data from
[`https://leaks.zamanalwsl.net/martyrs.php`](https://leaks.zamanalwsl.net/martyrs.php).
The script issues search requests for a range of keywords, parses the resulting
HTML tables and stores the rows in a CSV file.

## Setup

Install the required packages in a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the scraper using Python. The output will be stored in
`martyrs_data.csv`.

```bash
python scrape_martyrs.py
```

The script loops through letters `a-z` and digits `0-9`, sending a request
for each term. If the website changes or uses a different query parameter,
you may need to modify the script.