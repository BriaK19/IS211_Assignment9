"""
football_stats.py
Scrape NFL Touchdown Leaders (Top 20)
Source (scraped via NFL stats feed):
https://site.web.api.espn.com/apis/v2/sports/football/nfl/athletes
"""

import requests

URL = "https://site.web.api.espn.com/apis/v2/sports/football/nfl/athletes?limit=200"

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
data = response.json()

players = [ ]

# Extract TD stats if available
for item in data.get("items", []):
    name = item.get("fullName", "Unknown")
    team = item.get("team", {}).get("abbreviation", "N/A")
    pos = item.get("position", {}).get("abbreviation", "N/A")

    stats = item.get("stats", {})
    touchdowns = stats.get("touchdowns") or stats.get("tds") or 0

    if touchdowns and touchdowns != 0:
        players.append((name, pos, team, touchdowns))

# Sort by touchdowns (highest first)
players.sort(key=lambda x: x[3], reverse=True)

print("Rank, Player, Position, Team, TDs")
for i, p in enumerate(players[:20], start=1):
    print(f"{i}, {p[0]}, {p[1]}, {p[2]}, {p[3]}")

