import csv
import string
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://leaks.zamanalwsl.net/martyrs.php"


def fetch(keyword: str) -> str:
    """Retrieve HTML for a search keyword."""
    params = {"search": keyword}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.text


def parse_html(html: str):
    """Parse HTML table and return a list of row dictionaries."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []

    header_cells = table.find("tr").find_all(["th", "td"])
    headers = [cell.get_text(strip=True) for cell in header_cells]

    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        if cells:
            rows.append(dict(zip(headers, cells)))
    return rows


def scrape_all():
    """Iterate over multiple search queries and collect all results."""
    results = []
    search_terms = list(string.ascii_lowercase) + list(string.digits)
    for term in search_terms:
        html = fetch(term)
        rows = parse_html(html)
        results.extend(rows)
    return results


def save_to_csv(rows, filename: str):
    """Save scraped rows to a CSV file."""
    if not rows:
        return
    headers = rows[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    data = scrape_all()
    save_to_csv(data, "martyrs_data.csv")
    print(f"Saved {len(data)} rows to martyrs_data.csv")
