import requests
from bs4 import BeautifulSoup
from apps.mpl_api.utils import BasePathProvider


import logging

class MPLStandingsIDScraper:

    URL = BasePathProvider.get_mpl_id_path()

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        html = response.text
        # Debug: log the first 500 characters of the HTML
        logging.warning("Fetched HTML (first 500 chars):\n%s", html[:500])
        return html

    def parse_standings(self, html):
        soup = BeautifulSoup(html, "html.parser")
        # Find the regular season standings tab content
        tab_content = soup.find("div", {"id": "standing-regular-season"})
        if not tab_content:
            logging.warning("Tab content for regular season standings not found!")
            return []
        # Find the first table with class 'table-standings' in the tab content
        table = tab_content.find("table", class_="table-standings")
        if not table:
            logging.warning("Standings table not found in tab content!")
            return []

        standings = []
        for row in table.tbody.find_all("tr"):
            team_info = row.find("td", class_="team-info")
            if not team_info:
                continue

            rank = team_info.find("div", class_="team-rank").text.strip()
            logo = team_info.find("img")["src"]
            name = team_info.find("span", class_="d-none d-lg-block").text.strip()

            cells = row.find_all("td")
            match_point = cells[1].text.strip()
            match_wl = cells[2].text.strip().replace("\n", "").replace(" ", "")
            net_game_win = cells[3].text.strip()
            game_wl = cells[4].text.strip().replace("\n", "").replace(" ", "")

            standings.append({
                "rank": int(rank),
                "team_name": name,
                "team_logo": logo,
                "match_point": int(match_point),
                "match_wl": match_wl,
                "net_game_win": int(net_game_win),
                "game_wl": game_wl,
            })
        logging.warning("Parsed %d standings rows", len(standings))
        return standings

    def get_standings(self):
        html = self.fetch_html()
        return self.parse_standings(html)