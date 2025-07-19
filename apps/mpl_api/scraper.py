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
    
class MPLIDTransferScraper:
    base_url = BasePathProvider.get_mpl_id_path()
    URL = f"{base_url}transfer"

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        return response.text

    def clean_team_name(self, name):
        # Remove excessive whitespace and newlines, keep (MDL)/(MPL) if present
        if not name:
            return None
        name = name.replace('\n', '').strip()
        # Collapse multiple spaces
        name = ' '.join(name.split())
        return name

    def parse_transfers(self, html):
        soup = BeautifulSoup(html, "html.parser")
        transfers = []
        # Find all transfer cards
        for card in soup.find_all("div", class_="transfer-card"):
            transfer = {}

            # Date
            date_div = card.find("div", class_="col-lg-2")
            transfer_date = date_div.get_text(strip=True) if date_div else None

            # Player name and role
            player_info_div = card.find("div", class_="col-lg-4")
            player_name = None
            player_role = None
            if player_info_div:
                name_div = player_info_div.find("div", style=lambda v: v and "font-weight: 600" in v)
                role_div = player_info_div.find("div", style=lambda v: v and "font-size: .8rem;" in v)
                player_name = name_div.get_text(strip=True) if name_div else None
                player_role = role_div.get_text(strip=True) if role_div else None

            # From team
            from_team_div = card.find_all("div", class_="col-lg-5")
            from_team_logo = None
            from_team_name = None
            to_team_logo = None
            to_team_name = None
            if len(from_team_div) >= 2:
                from_team = from_team_div[0]
                logo_tag = from_team.find("img", class_="logo")
                from_team_logo = logo_tag["src"].strip() if logo_tag else None
                name_div = from_team.find("div", class_="team-name")
                from_team_name = self.clean_team_name(name_div.get_text()) if name_div else None

                # To team
                to_team = from_team_div[1]
                logo_tag = to_team.find("img", class_="logo")
                to_team_logo = logo_tag["src"].strip() if logo_tag else None
                name_div = to_team.find("div", class_="team-name")
                to_team_name = self.clean_team_name(name_div.get_text()) if name_div else None
            else:
                from_team_logo = from_team_name = to_team_logo = to_team_name = None

            transfer.update({
                "transfer_date": transfer_date,
                "player_name": player_name,
                "player_role": player_role,
                "from_team_name": from_team_name,
                "from_team_logo": from_team_logo,
                "to_team_name": to_team_name,
                "to_team_logo": to_team_logo,
            })
            transfers.append(transfer)
        logging.warning("Parsed %d transfers", len(transfers))
        return transfers

    def get_transfers(self):
        html = self.fetch_html()
        return self.parse_transfers(html)
    
class MPLIDStatisticsScraper:
    base_url = BasePathProvider.get_mpl_id_path()
    URL = f"{base_url}statistics"

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        return response.text

    def parse_team_statistics(self, html):
        soup = BeautifulSoup(html, "html.parser")
        team_stats = []
        # Find the team statistics table
        table = soup.find("table", id="table-team-statistics")
        if not table:
            logging.warning("Team statistics table not found!")
            return team_stats

        for row in table.tbody.find_all("tr"):
            team_info_td = row.find("td", class_="team-info")
            if not team_info_td:
                continue

            # Extract team logo
            logo_div = team_info_td.find("div", class_="team-logo")
            logo_img = logo_div.find("img") if logo_div else None
            team_logo = logo_img["src"].strip() if logo_img and logo_img.has_attr("src") else None

            # Extract team name (prefer d-lg-block for full name)
            name_div = team_info_td.find("div", class_="team-name")
            team_name = None
            if name_div:
                span_full = name_div.find("span", class_="d-none d-lg-block")
                if span_full and span_full.text.strip():
                    team_name = span_full.text.strip()
                else:
                    span_short = name_div.find("span", class_="d-lg-none")
                    team_name = span_short.text.strip() if span_short else None

            cells = row.find_all("td")
            # cells[0] is team-info, the rest are team_stats
            if len(cells) < 9:
                continue  # Not enough columns

            def parse_int(val):
                return int(val.replace(",", "").replace(".", "")) if val else 0

            team_stats.append({
                "team_name": team_name,
                "team_logo": team_logo,
                "kills": parse_int(cells[1].text.strip()),
                "deaths": parse_int(cells[2].text.strip()),
                "assists": parse_int(cells[3].text.strip()),
                "gold": parse_int(cells[4].text.strip()),
                "damage": parse_int(cells[5].text.strip()),
                "lord": parse_int(cells[6].text.strip()),
                "tortoise": parse_int(cells[7].text.strip()),
                "tower": parse_int(cells[8].text.strip()),
            })
        logging.warning("Parsed %d team statistics rows", len(team_stats))
        return team_stats