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
    
class MPLIDStatsScraper:
    base_url = BasePathProvider.get_mpl_id_path()
    URL = f"{base_url}statistics"

    def fetch_html(self):
        response = requests.get(self.URL)
        response.raise_for_status()
        return response.text

    def parse_team_stats(self, html):
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
    
    def parse_player_stats(self, html):
        soup = BeautifulSoup(html, "html.parser")
        player_stats = []
        # Find the player statistics table
        table = soup.find("table", class_="table-players-statistics")
        if not table:
            logging.warning("Player statistics table not found!")
            return player_stats

        for row in table.tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 11:
                continue

            # Player info (logo and name)
            player_td = cells[0]
            logo_img = player_td.find("img")
            player_logo = logo_img["src"].strip() if logo_img and logo_img.has_attr("src") else None
            name_div = player_td.find("div", class_="player-name")
            player_name = name_div.get_text(strip=True) if name_div else None

            def parse_int(val):
                try:
                    return int(val.replace(",", "").replace(".", ""))
                except Exception:
                    return 0

            def parse_float(val):
                try:
                    return float(val.replace(",", ".").replace("%", "").strip())
                except Exception:
                    return 0.0

            player_stats.append({
                "player_name": player_name,
                "player_logo": player_logo,
                "lane": cells[1].get_text(strip=True),
                "total_games": parse_int(cells[2].get_text(strip=True)),
                "total_kills": parse_int(cells[3].get_text(strip=True)),
                "avg_kills": parse_float(cells[4].get_text(strip=True)),
                "total_deaths": parse_int(cells[5].get_text(strip=True)),
                "avg_deaths": parse_float(cells[6].get_text(strip=True)),
                "total_assists": parse_int(cells[7].get_text(strip=True)),
                "avg_assists": parse_float(cells[8].get_text(strip=True)),
                "avg_kda": parse_float(cells[9].get_text(strip=True)),
                "kill_participation": cells[10].get_text(strip=True),
            })
        logging.warning("Parsed %d player statistics rows", len(player_stats))
        return player_stats
    
    def parse_hero_stats(self, html):
        soup = BeautifulSoup(html, "html.parser")
        hero_stats = []
        # Find the hero statistics table
        table = soup.find("table", id="table-heroes-statistics")
        if not table:
            logging.warning("Hero statistics table not found!")
            return hero_stats

        for row in table.tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 5:
                continue

            # Hero info (logo and name)
            hero_td = cells[0]
            logo_img = hero_td.find("img")
            hero_logo = logo_img["src"].strip() if logo_img and logo_img.has_attr("src") else None
            name_div = hero_td.find("div", class_="hero-name")
            hero_name = name_div.get_text(strip=True) if name_div else None

            def parse_int(val):
                try:
                    return int(val.replace(",", "").replace(".", "").replace(" ", ""))
                except Exception:
                    return 0

            def parse_percent(val):
                try:
                    return float(val.replace("%", "").replace(",", ".").strip())
                except Exception:
                    return 0.0

            hero_stats.append({
                "hero_name": hero_name,
                "hero_logo": hero_logo,
                "pick": parse_int(cells[1].get_text(strip=True)),
                "ban": parse_int(cells[2].get_text(strip=True)),
                "win": parse_int(cells[3].get_text(strip=True)),
                "win_rate": parse_percent(cells[4].get_text(strip=True)),
            })
        logging.warning("Parsed %d hero statistics rows", len(hero_stats))
        return hero_stats
    
    def parse_hero_pools(self, html):
        soup = BeautifulSoup(html, "html.parser")
        hero_pools = []
        # Find the hero pools table (id can be "table-hero-pools" or "table-heroes-pools")
        table = soup.find("table", id="table-hero-pools") or soup.find("table", id="table-heroes-pools")
        if not table:
            logging.warning("Hero pools table not found!")
            return hero_pools

        for row in table.tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            # Player info
            player_td = cells[0]
            team_logo_img = player_td.find("img")
            team_logo = team_logo_img["src"].strip() if team_logo_img and team_logo_img.has_attr("src") else None
            player_name_div = player_td.find("div", class_="player-name")
            player_name = player_name_div.get_text(strip=True) if player_name_div else None

            # Lane
            lane = cells[1].get_text(strip=True)

            # Total heroes
            try:
                total_heroes = int(cells[2].get_text(strip=True))
            except Exception:
                total_heroes = 0

            # Hero pool details
            hero_pool_cell = cells[3]
            hero_pool_outer = hero_pool_cell.find("div", class_="hero-pool-outer")
            hero_list = []
            if hero_pool_outer:
                for hero_div in hero_pool_outer.find_all("div", class_="position-relative"):
                    hero_img = hero_div.find("img", class_="hero-pool-image")
                    hero_logo = hero_img["src"].strip() if hero_img and hero_img.has_attr("src") else None
                    pick_div = hero_div.find("div", class_="hero-pool-pick")
                    try:
                        pick = int(pick_div.get_text(strip=True)) if pick_div else 0
                    except Exception:
                        pick = 0
                    count_div = hero_div.find("div", class_="hero-pool-count")
                    try:
                        pick_rate = float(count_div.get_text(strip=True).replace("%", "").replace(",", ".").strip()) if count_div else 0.0
                    except Exception:
                        pick_rate = 0.0
                    hero_list.append({
                        "hero_logo": hero_logo,
                        "pick": pick,
                        "pick_rate": pick_rate,
                    })

            hero_pools.append({
                "player_name": player_name,
                "team_logo": team_logo,
                "lane": lane,
                "total_heroes": total_heroes,
                "hero_pool": hero_list,
            })
        logging.warning("Parsed %d hero pools rows", len(hero_pools))
        return hero_pools
    
    def parse_player_pools(self, html):
        soup = BeautifulSoup(html, "html.parser")
        player_pools = []
        table = soup.find("table", id="table-player-pools")
        if not table:
            logging.warning("Player pools table not found!")
            return player_pools

        for row in table.tbody.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) < 3:
                continue

            # Hero info
            hero_td = cells[0]
            hero_img = hero_td.find("img", class_="hero-image")
            hero_logo = hero_img["src"].strip() if hero_img and hero_img.has_attr("src") else None
            hero_name_div = hero_td.find("div", class_="hero-name")
            hero_name = hero_name_div.get_text(strip=True) if hero_name_div else None

            # Total
            try:
                total = int(cells[1].get_text(strip=True))
            except Exception:
                total = 0

            # Players
            players_cell = cells[2]
            player_pool_outer = players_cell.find("div", class_="player-pool-outer")
            players = []
            if player_pool_outer:
                for player_card in player_pool_outer.find_all("div", class_="player-pool-card"):
                    player_img_outer = player_card.find("div", class_="player-pool-image-outer")
                    player_img = player_img_outer.find("img", class_="player-pool-image") if player_img_outer else None
                    player_logo = player_img["src"].strip() if player_img and player_img.has_attr("src") else None

                    player_info_div = player_card.find("div", class_="player-pool-info")
                    player_info = player_info_div.get_text(strip=True) if player_info_div else None

                    pick_div = player_card.find("div", class_="player-pool-pick")
                    try:
                        pick = int(pick_div.get_text(strip=True)) if pick_div else 0
                    except Exception:
                        pick = 0

                    count_div = player_card.find("div", class_="player-pool-count")
                    try:
                        pick_rate = float(count_div.get_text(strip=True).replace("%", "").replace(",", ".").strip()) if count_div else 0.0
                    except Exception:
                        pick_rate = 0.0

                    players.append({
                        "player_logo": player_logo,
                        "player_info": player_info,
                        "pick": pick,
                        "pick_rate": pick_rate,
                    })

            player_pools.append({
                "hero_name": hero_name,
                "hero_logo": hero_logo,
                "total": total,
                "players": players,
            })
        logging.warning("Parsed %d player pools rows", len(player_pools))
        return player_pools
    
    def parse_mvp_standings(self, html):
        soup = BeautifulSoup(html, "html.parser")
        mvp_standings = []
        # Find the MVP standings tab content
        tab_content = soup.find("div", id="mvp-standings")
        if not tab_content:
            logging.warning("MVP standings tab content not found!")
            return mvp_standings

        # Find all MVP cards
        for card in tab_content.find_all("div", class_="mvp-card"):
            mvp = {}

            # Team logo
            team_logo_div = card.find("div", class_="team-logo")
            team_logo_img = team_logo_div.find("img") if team_logo_div else None
            team_logo = team_logo_img["src"].strip() if team_logo_img and team_logo_img.has_attr("src") else None

            # Player image
            player_image_div = card.find("div", class_="player-image")
            player_image_img = player_image_div.find("img") if player_image_div else None
            player_logo = player_image_img["src"].strip() if player_image_img and player_image_img.has_attr("src") else None

            # Rank
            rank_div = card.find("div", class_="rank")
            rank = rank_div.get_text(strip=True).replace("#", "") if rank_div else None

            # Points
            point_div = card.find("div", class_="point")
            point_text = point_div.get_text(strip=True) if point_div else ""
            point = None
            if point_text:
                try:
                    point = int(point_text.split()[0])
                except Exception:
                    point = None

            # Player name
            name_div = card.find("div", class_="mvp-ign")
            player_name = name_div.get_text(strip=True) if name_div else None

            mvp.update({
                "rank": int(rank) if rank and rank.isdigit() else None,
                "player_name": player_name,
                "player_logo": player_logo,
                "team_logo": team_logo,
                "point": point,
            })
            mvp_standings.append(mvp)
        logging.warning("Parsed %d MVP standings cards", len(mvp_standings))
        return mvp_standings