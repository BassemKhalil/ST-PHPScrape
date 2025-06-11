# ST-PHPScrape

This repository contains a simple Python script to collect data from
[`https://leaks.zamanalwsl.net/martyrs.php`](https://leaks.zamanalwsl.net/martyrs.php).
The script issues search requests for a range of Arabic letters, parses the
resulting HTML tables and stores the rows in a CSV file.

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

The script loops through the standard Arabic alphabet, sending a request for
each first-letter search. If the website changes or introduces new query
parameters, you may need to adjust the code accordingly.
