import sys
import json
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
HDRS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def epoch_to_ymd(sec: int) -> str:
    return datetime.utcfromtimestamp(sec).strftime("%Y-%m-%d")

def main():
    try:
        resp = requests.get(URL, headers=HDRS, timeout=25)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching Yahoo page: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")

    # Find the script tag that contains HistoricalPriceStore JSON
    data_script = None
    for sc in soup.find_all("script"):
        txt = sc.string or ""
        if "HistoricalPriceStore" in txt:
            data_script = txt
            break

    if not data_script:
        print("Could not find HistoricalPriceStore JSON. Page structure may have changed.")
        sys.exit(2)

    # Extract JSON substring robustly
    try:
        start = data_script.index('{"context"')
        end = data_script.rindex("}") + 1
        payload = json.loads(data_script[start:end])
    except Exception as e:
        print(f"Failed parsing embedded JSON: {e}", file=sys.stderr)
        sys.exit(3)

    # Navigate to the prices array
    try:
        store = payload["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]
        prices = store["prices"]
    except Exception as e:
        print(f"Unexpected JSON structure: {e}", file=sys.stderr)
        sys.exit(4)

    print("Date, Close")
    for row in prices:
        # Skip event rows (splits/dividends) that don't have 'type' None and 'close'
        if row.get("type") is not None:
            continue
        if "date" not in row or "close" not in row:
            continue
        date_str = epoch_to_ymd(int(row["date"]))
        close = row["close"]
        # Some rows might have null close (skip)
        if close is None:
            continue
        print(f"{date_str}, {close}")

if __name__ == "__main__":
    main()
