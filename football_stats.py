import sys
import requests
from bs4 import BeautifulSoup

URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/qualifiers/"

HDRS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0 Safari/537.36"
}

def find_scoring_table(soup: BeautifulSoup):
    """
    CBS frequently renders stat tables with a THEAD of column headers and a TBODY of rows.
    We locate a table whose headers include 'TD' and 'Player'.
    """
    tables = soup.find_all("table")
    for tbl in tables:
        # Read headers from thead (preferred) or first row
        headers = []
        thead = tbl.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find_all("th")]
        else:
            first_tr = tbl.find("tr")
            if first_tr:
                headers = [th.get_text(strip=True) for th in first_tr.find_all(["th", "td"])]

        lowered = [h.lower() for h in headers]
        if any("td" == h or "touchdowns" in h for h in lowered) and "player" in lowered:
            return tbl, headers
    return None, None

def main():
    try:
        r = requests.get(URL, headers=HDRS, timeout=20)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching CBS page: {e}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

    table, headers = find_scoring_table(soup)
    if table is None:
        print("Could not locate scoring table (headers with Player + TD). The site layout may have changed.")
        sys.exit(2)

    # Map columns we care about
    hdr_map = {h.lower(): i for i, h in enumerate(headers)}
    # Be flexible with naming variations
    def col_idx(*candidates):
        for c in candidates:
            # exact
            if c in hdr_map:
                return hdr_map[c]
        # fuzzy contains
        for k, i in hdr_map.items():
            if any(c in k for c in candidates):
                return i
        return None

    idx_player = col_idx("player")
    idx_pos    = col_idx("pos", "position")
    idx_team   = col_idx("team", "tm")
    idx_td     = col_idx("td", "touchdowns", "tot td", "total td")

    if any(x is None for x in (idx_player, idx_pos, idx_team, idx_td)):
        print("Found table but couldn't align expected columns (Player/Pos/Team/TD).")
        sys.exit(3)

    # Extract rows from tbody
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    print("Rank, Player, Position, Team, TDs")
    rank = 1
    for tr in rows:
        tds = tr.find_all(["td", "th"])
        if len(tds) < max(idx_player, idx_pos, idx_team, idx_td) + 1:
            continue

        player = tds[idx_player].get_text(" ", strip=True)
        pos    = tds[idx_pos].get_text(" ", strip=True)
        team   = tds[idx_team].get_text(" ", strip=True)
        tds_val = tds[idx_td].get_text(" ", strip=True)

        # Skip non-player or blank rows
        if not player or player.lower() in {"player"}:
            continue

        print(f"{rank}, {player}, {pos}, {team}, {tds_val}")
        rank += 1
        if rank > 20:
            break

if __name__ == "__main__":
    main()
