# Week 9 Web Scraping Assignment – IS211

This repository contains two Python scripts that scrape and display data from external websites using `requests` and `BeautifulSoup`/JSON.

## 📌 Files Included

| Script | Description | Source |
|--------|-------------|--------|
| `wikipedia_superbowl.py` | Scrapes the Super Bowl Champions table from Wikipedia and prints the first 20 rows showing: Rank, Season, Winner, Score, Loser | https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions |
| `apple_stock.py` | Retrieves Apple (AAPL) historical stock closing prices using Yahoo Finance’s chart API and prints a `Date, Close` list | https://query2.finance.yahoo.com/v8/finance/chart/AAPL |

---

## ✅ How to Run

From the project folder, run:

```bash
python3 wikipedia_superbowl.py
python3 apple_stock.py
