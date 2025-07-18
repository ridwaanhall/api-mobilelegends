import requests
from bs4 import BeautifulSoup
from apps.mpl_api.utils import BasePathProvider

import logging

class MPLIDStandingsScraper:

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
    
class MPLIDTeamScraper:
    base_url = BasePathProvider.get_mpl_id_path()
    URL = f"{base_url}teams"

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        html = response.text
        # Debug: log the first 500 characters of the HTML
        logging.warning("Fetched HTML (first 500 chars):\n%s", html[:500])
        return html

    def parse_teams(self, html):
        """
        Scrape team cards from the teams section (team url, logo, and name).
        Returns a list of dicts: { 'team_url', 'team_logo', 'team_name' }
        """
        soup = BeautifulSoup(html, "html.parser")
        teams = []
        # Find the main content div for teams
        content_wrap = soup.find("div", class_="content-wrap")
        if not content_wrap:
            logging.warning("Teams content-wrap not found!")
            return teams
        # Find all team-card-outer divs
        for card in content_wrap.find_all("div", class_="team-card-outer"):
            a_tag = card.find("a", href=True)
            if not a_tag:
                continue
            team_url = a_tag["href"].strip()
            img_tag = card.find("img", alt=True, src=True)
            team_logo = img_tag["src"].strip() if img_tag else None
            # Team name is in .team-name-inner
            name_div = card.find("div", class_="team-name-inner")
            team_name = name_div.text.strip() if name_div else None
            teams.append({
                "team_url": team_url,
                "team_logo": team_logo,
                "team_name": team_name,
            })
        logging.warning("Parsed %d team cards", len(teams))
        return teams
    
    def get_teams(self):
        html = self.fetch_html()
        return self.parse_teams(html)
    
class MPLIDTeamDetailScraper:
    base_url = BasePathProvider.get_mpl_id_path()
    URL = f"{base_url}team/{{team_id}}"

    def __init__(self, team_id):
        self.team_id = team_id
        self.URL = self.URL.format(team_id=team_id)

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        return response.text

    def parse_team_details(self, html):
        soup = BeautifulSoup(html, "html.parser")
        result = {}

        # Team name and logo
        h4 = soup.find("h4", class_="d-flex")
        if h4:
            logo_tag = h4.find("img", class_="team-logo")
            result["team_logo"] = logo_tag["src"].strip() if logo_tag else None
            # The team name is the text after the img tag
            name = h4.get_text(strip=True)
            result["team_name"] = name

        # Social media links
        socmed_div = soup.find("div", class_="icon-socmed")
        socmed = {}
        if socmed_div:
            for a in socmed_div.find_all("a", href=True):
                href = a["href"]
                icon = a.find("i")
                if icon and icon.get("class"):
                    for cls in icon["class"]:
                        if "facebook" in cls:
                            socmed["facebook"] = href
                        elif "instagram" in cls:
                            socmed["instagram"] = href
                        elif "youtube" in cls:
                            socmed["youtube"] = href
        result["social_media"] = socmed

        # Roster
        roster = []
        roster_section = soup.find("div", attrs={"data-ga-impression": "Section Roster Team Detail"})
        if roster_section:
            for player_div in roster_section.find_all("div", class_="col-md-3"):
                player = {}
                img_tag = player_div.find("img", alt=True, src=True)
                player["player_image"] = img_tag["src"].strip() if img_tag else None
                player_name_div = player_div.find("div", class_="player-name")
                player["player_name"] = player_name_div.get_text(strip=True) if player_name_div else None
                player_role_div = player_div.find("div", class_="player-role")
                player["player_role"] = player_role_div.get_text(strip=True) if player_role_div else None
                roster.append(player)
        result["roster"] = roster

        return result

    def get_team_details(self):
        html = self.fetch_html()
        return self.parse_team_details(html)