"""
football_stats.py
Scrape NFL TOTAL TOUCHDOWN LEADERS
Source:
https://www.pro-football-reference.com/years/2024/leaders/touchdowns_scoring.htm
"""

import requests
from bs4 import BeautifulSoup, Comment

URL = "https://www.pro-football-reference.com/years/2024/leaders/touchdowns_scoring.htm"
headers = {"User-Agent": "Mozilla/5.0"}

res = requests.get(URL, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

# Remove HTML comments so table becomes accessible
for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
    comment.extract()

# Now find the touchdowns leaders table
table = soup.find("table", {"id": "leaders"})
tbody = table.find("tbody")
rows = tbody.find_all("tr")

print("Rank, Player, Team, TDs")
rank = 1

for row in rows:
    cols = row.find_all("td")
    if len(cols) < 3:
        continue

    player = cols[0].get_text(strip=True)
    team   = cols[1].get_text(strip=True)
    tds    = cols[2].get_text(strip=True)

    if not tds.isdigit():
        continue

    print(f"{rank}, {player}, {team}, {tds}")
    rank += 1
    if rank > 20:
        break
	
