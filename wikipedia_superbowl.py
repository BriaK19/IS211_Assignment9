"""
wikipedia_superbowl.py
Scrape the Super Bowl champions table from Wikipedia and print the first 20 rows.
Source: https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions
"""

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def pick_champions_table(soup: BeautifulSoup):
    """Return (table, headers) for the champions table by matching header names."""
    for tbl in soup.select("table.wikitable"):
        # read header cells from thead or the first row
        headers = []
        thead = tbl.find("thead")
        if thead:
            headers = [th.get_text(" ", strip=True) for th in thead.find_all("th")]
        else:
            fr = tbl.find("tr")
            if fr:
                headers = [c.get_text(" ", strip=True) for c in fr.find_all(["th","td"])]
        low = [h.lower() for h in headers]
        # champions table has these header signals
        if any("season" in h for h in low) and \
           (any("winning" in h for h in low) or any("winner" in h for h in low)) and \
           (any("losing" in h for h in low) or any("loser" in h for h in low)) and \
           any("score" in h for h in low):
            return tbl, headers
    return None, []

def col_index(headers, *needles):
    """find header index by contains-matching any of the needles (lowercased)."""
    low = [h.lower() for h in headers]
    for i, h in enumerate(low):
        if any(n in h for n in needles):
            return i
    return None

def main():
    r = requests.get(URL, headers=HEADERS, timeout=25)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    table, headers = pick_champions_table(soup)
    if table is None:
        print("Could not find the champions table on the page.")
        return

    # figure out the columns we need, regardless of exact phrasing
    idx_season = col_index(headers, "season", "year")
    idx_winner = col_index(headers, "winning team", "winner")
    idx_score  = col_index(headers, "score")
    idx_loser  = col_index(headers, "losing team", "loser")

    # some pages repeat headers in first row – prefer tbody
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

print("Rank, Season, Winner, Score, Loser")
rank = 1
for tr in rows:
    tds = tr.find_all(["td","th"])
    if len(tds) < 5:
        continue

    season = tds[1].get_text(" ", strip=True)
    winner = tds[2].get_text(" ", strip=True)
    score  = tds[3].get_text(" ", strip=True)
    loser  = tds[4].get_text(" ", strip=True)

    # Skip the header-ish row that starts with "Date" in the Season cell
    if season.lower().startswith("date"):
        continue

    print(f"{rank}, {season}, {winner}, {score}, {loser}")
    rank += 1
    if rank > 20:
        break
