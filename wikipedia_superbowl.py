"""
wikipedia_superbowl.py
Scrape the Super Bowl champions table from Wikipedia and print the first 20 rows.
Source URL: https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions
"""

import requests
from bs4 import BeautifulSoup

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def main():
    r = requests.get(URL, headers=HEADERS, timeout=25)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    # Find the first champions wikitable
    table = soup.find("table", class_="wikitable")
    if not table:
        print("Could not find the champions table.")
        return

    rows = table.find_all("tr")
    print("Rank, Season, Winner, Score, Loser")

    rank = 1
    for tr in rows[1:]:
        tds = tr.find_all(["td", "th"])
        if len(tds) < 5:
            continue
        season = tds[1].get_text(" ", strip=True)
        winner = tds[2].get_text(" ", strip=True)
        score  = tds[3].get_text(" ", strip=True)
        loser  = tds[4].get_text(" ", strip=True)

        print(f"{rank}, {season}, {winner}, {score}, {loser}")
        rank += 1
        if rank > 20:
            break

if __name__ == "__main__":
    main()
	
