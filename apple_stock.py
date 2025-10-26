"""
apple_stock.py
Scrape AAPL historical prices from Yahoo using the public chart API.
Primary (Yahoo JSON):
  https://query2.finance.yahoo.com/v8/finance/chart/AAPL?range=2y&interval=1d&includePrePost=false&events=div%2Csplit
This prints: Date, Close
"""

import requests
from datetime import datetime, timezone

CHART_URL = (
    "https://query2.finance.yahoo.com/v8/finance/chart/AAPL"
    "?range=2y&interval=1d&includePrePost=false&events=div%2Csplit"
)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def epoch_to_ymd(sec: int) -> str:
    return datetime.fromtimestamp(sec, tz=timezone.utc).strftime("%Y-%m-%d")

def main():
    r = requests.get(CHART_URL, headers=HEADERS, timeout=25)
    r.raise_for_status()
    data = r.json()

    result = data["chart"]["result"][0]
    ts = result.get("timestamp", []) or []
    # Prefer adjusted close if available; otherwise regular close
    adj = (result.get("indicators", {}).get("adjclose") or [{}])[0].get("adjclose")
    close = (result.get("indicators", {}).get("quote") or [{}])[0].get("close")

    series = adj if adj is not None else close
    if not ts or not series:
        raise RuntimeError("No time series returned by Yahoo chart API.")

    print("Date, Close")
    for t, c in zip(ts, series):
        if c is None:
            continue
        print(f"{epoch_to_ymd(int(t))}, {c}")

if __name__ == "__main__":
    main()

	
