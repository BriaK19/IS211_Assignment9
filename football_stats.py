"""
football_stats.py
Print TOP 20 NFL Touchdown leaders from CBS Sports (Regular Season)
Filters out Kickers and players with zero touchdowns.
URL used:
https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/
"""

import requests
from bs4 import BeautifulSoup

URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")

tbody = table.find("tbody")
rows = tbody.find_all("tr")

print("Rank, Player, Position, Team, TDs")
rank = 1

for tr in rows:
    cols = tr.find_all("td")
    if len(cols) < 7:
        continue

    player = cols[0].get_text(strip=True)
    pos = cols[1].get_text(strip=True)
    team = cols[2].get_text(strip=True)
    tds = cols[6].get_text(strip=True)  # TD column index

    # Skip kickers + players with no TDs recorded
    if pos == "K":
        continue
    if not any(ch.isdigit() for ch in tds):
        continue

    print(f"{rank}, {player}, {pos}, {team}, {tds}")
    rank += 1
    if rank > 20:
        break

	
