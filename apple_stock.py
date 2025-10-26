"""
apple_stock.py
Scrape AAPL Historical Data. Try HTML first; if blocked, use CSV fallback.
Sources:
- HTML: https://finance.yahoo.com/quote/AAPL/history?p=AAPL
- CSV : https://query1.finance.yahoo.com/v7/finance/download/AAPL
"""

import sys, json, time, csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

HTML_URL = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
CSV_URL  = "https://query1.finance.yahoo.com/v7/finance/download/AAPL"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

def epoch_to_ymd(sec: int) -> str:
    return datetime.utcfromtimestamp(sec).strftime("%Y-%m-%d")

def try_html():
    r = requests.get(HTML_URL, headers=HEADERS, timeout=25)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    blob = None
    for sc in soup.find_all("script"):
        txt = sc.string or ""
        if "HistoricalPriceStore" in txt:
            blob = txt; break
    if not blob:
        raise RuntimeError("HistoricalPriceStore JSON not found")
    start = blob.index('{"context"'); end = blob.rindex("}") + 1
    data = json.loads(blob[start:end])
    prices = data["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]["prices"]
    out = []
    for row in prices:
        if row.get("type") is not None: continue
        if row.get("close") is None or "date" not in row: continue
        out.append((epoch_to_ymd(int(row["date"])), row["close"]))
    if not out:
        raise RuntimeError("No price rows parsed from HTML JSON")
    return out

def try_csv(days=365):
    end = int(time.time()); start = end - days*24*3600
    params = {"period1": start, "period2": end, "interval": "1d", "events": "history", "includeAdjustedClose": "true"}
    r = requests.get(CSV_URL, params=params, headers=HEADERS, timeout=25)
    r.raise_for_status()
    rows = []
    for rec in csv.DictReader(r.text.splitlines()):
        if rec.get("Date") and rec.get("Close") and rec["Close"] not in ("null", ""):
            rows.append((rec["Date"], rec["Close"]))
    if not rows:
        raise RuntimeError("CSV returned no rows")
    return rows

def main():
    print("Date, Close")
    try:
        rows = try_html()
    except Exception as e:
        print(f"# HTML scrape failed ({e}); using CSV fallback.", file=sys.stderr)
        rows = try_csv()
    for d, c in rows:
        print(f"{d}, {c}")

if __name__ == "__main__":
    main()

	
