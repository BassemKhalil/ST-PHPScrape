import csv
import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://leaks.zamanalwsl.net/martyrs.php"
USER_AGENT = "Mozilla/5.0 (compatible; ST-PHPScrape/1.0)"

# Arabic alphabet used for first name searches
ARABIC_LETTERS = [
    "ا", "ب", "ت", "ث", "ج", "ح", "خ", "د",
    "ذ", "ر", "ز", "س", "ش", "ص", "ض", "ط",
    "ظ", "ع", "غ", "ف", "ق", "ك", "ل", "م",
    "ن", "ه", "و", "ي",
]


def fetch(letter: str, page: int = 1) -> str:
    """Retrieve HTML for a search letter and page number."""
    params = {"firstname": letter, "state": "", "page": page}
    headers = {"User-Agent": USER_AGENT}
    response = requests.get(BASE_URL, params=params, headers=headers)
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


def scrape_letter(letter: str):
    """Collect all results for a single letter across pages."""
    results = []
    page = 1
    while True:
        html = fetch(letter, page)
        rows = parse_html(html)
        if not rows:
            break
        results.extend(rows)

        soup = BeautifulSoup(html, "html.parser")
        next_page = page + 1
        if soup.find("a", href=lambda h: h and f"page={next_page}" in h):
            page += 1
            time.sleep(0.5)
        else:
            break
    return results


def scrape_all():
    """Iterate over Arabic letters and collect all results."""
    results = []
    for letter in ARABIC_LETTERS:
        rows = scrape_letter(letter)
        results.extend(rows)
        time.sleep(0.5)
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
