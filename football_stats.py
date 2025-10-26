"""
football_stats.py
Print top 20 NFL scoring leaders (Regular season) from CBS Sports:
Rank, Player, Position, Team, TDs
"""
import sys
import requests
from bs4 import BeautifulSoup
from datetime import datetime

PRIMARY = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/"
YR = datetime.now().year
FALLBACKS = [
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR}-season-regular-category-touchdowns",
    f"https://www.cbssports.com/nfl/stats/playersort/nfl/year-{YR-1}-season-regular-category-touchdowns",
]
HDRS = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"}

def fetch(url):
    r = requests.get(url, headers=HDRS, timeout=20)
    r.raise_for_status()
    return r.text

def locate_table(soup):
    for tbl in soup.find_all("table"):
        # headers
        thead = tbl.find("thead")
        headers = [th.get_text(strip=True) for th in thead.find_all("th")] if thead else []
        if not headers and tbl.find("tr"):
            headers = [c.get_text(strip=True) for c in tbl.find("tr").find_all(["th","td"])]
        low = [h.lower() for h in headers]
        if ("player" in " ".join(low)) and any(h in {"td","tds"} or "touchdown" in h for h in low):
            return tbl, headers
    return None, None

def col_idx(headers, *cands):
    hmap = {h.lower(): i for i, h in enumerate(headers)}
    for c in cands:
        if c in hmap: return hmap[c]
    for i, h in enumerate(headers):
        if any(c in h.lower() for c in cands): return i
    return None

def parse_and_print(table, headers):
    idx_p = col_idx(headers, "player")
    idx_pos = col_idx(headers, "pos", "position")
    idx_tm = col_idx(headers, "team", "tm")
    idx_td = col_idx(headers, "td", "tds", "touchdowns", "tot td", "total td")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]
    print("Rank, Player, Position, Team, TDs")
    rank = 1
    for tr in rows:
        tds = tr.find_all(["td","th"])
        if not tds: continue
        def get(i): return tds[i].get_text(" ", strip=True) if i is not None and i < len(tds) else ""
        player = get(idx_p)
        if not player or player.lower() == "player": continue
        pos, tm, tds_val = get(idx_pos) or "-", get(idx_tm) or "-", get(idx_td)
        print(f"{rank}, {player}, {pos}, {tm}, {tds_val}")
        rank += 1
        if rank > 20: break

def main():
    tried = []
    for url in [PRIMARY] + FALLBACKS:
        try:
            html = fetch(url)
            soup = BeautifulSoup(html, "html.parser")
            tbl, hdrs = locate_table(soup)
            if tbl:
                parse_and_print(tbl, hdrs)
                return
            tried.append(url)
        except Exception as e:
            tried.append(f"{url} (error: {e})")
    print("Could not locate CBS scoring table. Tried:")
    for t in tried: print(" -", t)
    sys.exit(2)

if __name__ == "__main__":
    main()


	
