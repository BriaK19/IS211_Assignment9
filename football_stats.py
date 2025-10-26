"""
football_stats.py
Outputs the TOP 20 NFL TOUCHDOWNS leaders (regular season) from CBS Sports.
Fields: Rank, Player, Position, Team, TDs

Primary (touchdowns) and year fallbacks are included.
"""

import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Prefer the "playersort ... category-touchdowns" endpoint (server-rendered HTML)
YR = datetime.now().year
URLS = [
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR}-season-regular-category-touchdowns",
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR-1}-season-regular-category-touchdowns",
    # Keep the “qualifiers” page last just in case
    "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/",
]

HDRS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
}

def fetch_html(url):
    r = requests.get(url, headers=HDRS, timeout=25)
    r.raise_for_status()
    return r.text

def locate_table(soup: BeautifulSoup):
    """Find a table whose headers include Player and a TD/Touchdowns/Tot column."""
    for tbl in soup.find_all("table"):
        # headers from thead or first row
        headers = []
        thead = tbl.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
        else:
            fr = tbl.find("tr")
            if fr:
                headers = [c.get_text(strip=True) for c in fr.find_all(["th", "td"])]

        low = [h.lower() for h in headers]
        has_player = any("player" in h for h in low)
        has_td = any(h in {"td", "tds", "tot", "tot td"} or "touchdown" in h for h in low)
        if has_player and has_td:
            return tbl, headers
    return None, None

def col_idx(headers, *cands):
    """Return header index by exact or contains match."""
    hmap = {h.lower(): i for i, h in enumerate(headers)}
    for c in cands:
        if c in hmap:
            return hmap[c]
    for i, h in enumerate(headers):
        hl = h.lower()
        if any(c in hl for c in cands):
            return i
    return None

def first_link_text(cell):
    a = cell.find("a")
    if a:
        return a.get_text(" ", strip=True)
    return cell.get_text(" ", strip=True)

def parse_and_print(table, headers):
    """Extract top-20 TD leaders."""
    idx_player = col_idx(headers, "player")
    idx_pos    = col_idx(headers, "pos", "position")
    idx_team   = col_idx(headers, "team", "tm")
    idx_td     = col_idx(headers, "tot td", "tot", "tds", "td", "touchdowns", "total td")

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    print("Rank, Player, Position, Team, TDs")
    rank = 1
    for tr in rows:
        tds = tr.find_all(["td", "th"])
        if not tds:
            continue

        # Some CBS tables duplicate visible text; prefer specific child elements.
        player = first_link_text(tds[idx_player]) if idx_player is not None else ""
        pos    = tds[idx_pos].get_text(" ", strip=True) if idx_pos is not None else "-"
        team   = tds[idx_team].get_text(" ", strip=True) if idx_team is not None else "-"

        # TD column name varies; grab numeric-looking value
        td_raw = tds[idx_td].get_text(" ", strip=True) if idx_td is not None else ""
        td_val = next((p for p in td_raw.replace("\u2014","-").split() if p.replace(".","",1).isdigit()), td_raw)

        if not player or player.lower() == "player":
            continue

        print(f"{rank}, {player}, {pos or '-'}, {team or '-'}, {td_val}")
        rank += 1
        if rank > 20:
            break

def main():
    tried = []
    for url in URLS:
        try:
            html = fetch_html(url)
            soup = BeautifulSoup(html, "html.parser")
            table, headers = locate_table(soup)
            if table:
                parse_and_print(table, headers)
                return
            tried.append(url + " (no matching headers)")
        except Exception as e:
            tried.append(f"{url} (error: {e})")

    print("Could not extract Touchdowns leaders. Tried:")
    for t in tried:
        print(" -", t)
    sys.exit(2)

if __name__ == "__main__":
    main()


	
