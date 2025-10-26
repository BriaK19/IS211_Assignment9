football_stats.py
Print TOP 20 NFL Touchdowns leaders (Regular season) from CBS Sports.
Avoids kicker tables by scoring candidate tables and choosing the best match.
"""

import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

YR = datetime.now().year
URLS = [
    # Server-rendered pages that list total touchdowns
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR}-season-regular-category-touchdowns",
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR-1}-season-regular-category-touchdowns",
    # Keep the generic page as a last resort
    "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/",
]

HDRS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

def fetch(url):
    r = requests.get(url, headers=HDRS, timeout=25)
    r.raise_for_status()
    return r.text

def get_headers(table):
    thead = table.find("thead")
    if thead:
        return [th.get_text(strip=True) for th in thead.find_all("th")]
    fr = table.find("tr")
    return [c.get_text(strip=True) for c in fr.find_all(["th","td"])] if fr else []

def col_idx(headers, *cands):
    hmap = {h.lower(): i for i, h in enumerate(headers)}
    for c in cands:
        if c in hmap: return hmap[c]
    for i, h in enumerate(headers):
        hl = h.lower()
        if any(c in hl for c in cands):
            return i
    return None

def table_score(table, headers):
    """Score how much this looks like TOTAL TOUCHDOWNS leaders (not kickers)."""
    low = [h.lower() for h in headers]
    if not any("player" in h for h in low):
        return -1
    # must have a TD-ish column
    if not any(h in {"td","tds","tot","tot td"} or "touchdown" in h for h in low):
        return -1

    idx_pos = col_idx(headers, "pos", "position")
    idx_td  = col_idx(headers, "tot td", "tot", "tds", "td", "touchdowns", "total td")

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    if idx_td is None or not rows:
        return -1

    non_k = 0
    td_numeric = 0
    checked = 0
    for tr in rows[:25]:
        tds = tr.find_all(["td","th"])
        if not tds: continue
        if idx_pos is not None and idx_pos < len(tds):
            pos = tds[idx_pos].get_text(" ", strip=True).upper()
            if pos and pos != "K":
                non_k += 1
        # count rows where TD looks numeric
        if idx_td < len(tds):
            val = tds[idx_td].get_text(" ", strip=True).replace("—","-").strip()
            if any(ch.isdigit() for ch in val):
                td_numeric += 1
        checked += 1

    if checked == 0:
        return -1

    # score favors tables with many non-K rows and numeric TDs
    return (non_k * 2) + td_numeric

def pick_best_table(soup):
    best = (None, None, -1)
    for tbl in soup.find_all("table"):
        headers = get_headers(tbl)
        score = table_score(tbl, headers)
        if score > best[2]:
            best = (tbl, headers, score)
    return best[0], best[1]

def parse_and_print(table, headers):
    idx_player = col_idx(headers, "player")
    idx_pos    = col_idx(headers, "pos", "position")
    idx_team   = col_idx(headers, "team", "tm")
    idx_td     = col_idx(headers, "tot td", "tot", "tds", "td", "touchdowns", "total td")

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    def first_link_text(cell):
        a = cell.find("a")
        return a.get_text(" ", strip=True) if a else cell.get_text(" ", strip=True)

    print("Rank, Player, Position, Team, TDs")
    rank = 1
    for tr in rows:
        tds = tr.find_all(["td","th"])
        if not tds: continue
        player = first_link_text(tds[idx_player]) if idx_player is not None else ""
        if not player or player.lower() == "player": continue
        pos  = tds[idx_pos].get_text(" ", strip=True) if idx_pos is not None else "-"
        team = tds[idx_team].get_text(" ", strip=True) if idx_team is not None else "-"
        raw  = tds[idx_td].get_text(" ", strip=True) if idx_td is not None else ""
        # pull the first numeric token as TDs
        td_val = next((tok for tok in raw.replace("—","-").split() if any(ch.isdigit() for ch in tok)), raw)
        print(f"{rank}, {player}, {pos or '-'}, {team or '-'}, {td_val}")
        rank += 1
        if rank > 20: break

def main():
    tried = []
    for url in URLS:
        try:
            html = fetch(url)
            soup = BeautifulSoup(html, "html.parser")
            table, headers = pick_best_table(soup)
            if table:
                parse_and_print(table, headers)
                return
            tried.append(url + " (no usable table)")
        except Exception as e:
            tried.append(f"{url} (error: {e})")

    print("Could not extract Touchdowns leaders. Tried:")
    for t in tried:
        print(" -", t)
    sys.exit(2)

if __name__ == "__main__":
    main()

	
