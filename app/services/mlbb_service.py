"""
MLBB Service Layer

This module handles business logic for interacting with the MLBB API.
"""

from typing import Dict, Any, Optional
from requests.exceptions import RequestException

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import BasePathProvider
from app.utils.http_client import HTTPClient, build_mlbb_headers

logger = get_logger(__name__)


class MLBBService:
    """Service for interacting with MLBB API."""
    
    def __init__(self):
        """Initialize MLBB service."""
        self.base_url = settings.MLBB_URL
        self.client = HTTPClient(self.base_url)
        self.base_path_provider = BasePathProvider(settings.SECRET_KEY)
        self._base_path: Optional[str] = None
    
    @property
    def base_path(self) -> str:
        """
        Get base path (cached).
        
        Returns:
            str: Base path for API endpoints
        """
        if self._base_path is None:
            self._base_path = self.base_path_provider.get_base_path()
        return self._base_path
    
    def _build_endpoint(self, path_suffix: str) -> str:
        """
        Build complete endpoint URL.
        
        Args:
            path_suffix: Path suffix to append
            
        Returns:
            str: Complete endpoint URL
        """
        return f"{self.base_path}/{path_suffix}"
    
    async def fetch_hero_list(
        self,
        lang: str = "en",
        page_size: int = 10000,
        page_index: int = 1
    ) -> Dict[str, Any]:
        """
        Fetch hero list from MLBB API.
        
        Args:
            lang: Language code
            page_size: Number of items per page
            page_index: Page index
            
        Returns:
            Dict[str, Any]: Hero list data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756564")
        
        payload = {
            "pageSize": page_size,
            "sorts": [
                {
                    "data": {"field": "hero_id", "order": "desc"},
                    "type": "sequence"
                }
            ],
            "pageIndex": page_index,
            "fields": [
                "hero_id",
                "hero.data.head",
                "hero.data.name",
                "hero.data.smallmap",
            ]
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero list: {e}")
            raise
    
    async def fetch_hero_rank(
        self,
        days: str,
        rank: str,
        page_size: int,
        page_index: int,
        sort_field: str,
        sort_order: str,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero rank data.
        
        Args:
            days: Time period (1, 3, 7, 15, 30)
            rank: Rank tier
            page_size: Number of items per page
            page_index: Page index
            sort_field: Field to sort by
            sort_order: Sort order (asc/desc)
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero rank data
            
        Raises:
            RequestException: If request fails
        """
        # Map days to endpoints
        endpoint_map = {
            "1": self._build_endpoint("2756567"),
            "3": self._build_endpoint("2756568"),
            "7": self._build_endpoint("2756569"),
            "15": self._build_endpoint("2756565"),
            "30": self._build_endpoint("2756570"),
        }
        
        # Map ranks to values
        rank_map = {
            "all": "101",
            "epic": "5",
            "legend": "6",
            "mythic": "7",
            "honor": "8",
            "glory": "9",
        }
        
        # Map sort fields
        sort_field_map = {
            "pick_rate": "main_hero_appearance_rate",
            "ban_rate": "main_hero_ban_rate",
            "win_rate": "main_hero_win_rate",
        }
        
        endpoint = endpoint_map.get(days, endpoint_map["1"])
        rank_value = rank_map.get(rank, "101")
        mapped_sort_field = sort_field_map.get(sort_field, "main_hero_win_rate")
        
        payload = {
            "pageSize": page_size,
            "filters": [
                {"field": "bigrank", "operator": "eq", "value": rank_value},
                {"field": "match_type", "operator": "eq", "value": "0"}
            ],
            "sorts": [
                {
                    "data": {"field": mapped_sort_field, "order": sort_order},
                    "type": "sequence"
                }
            ],
            "pageIndex": page_index,
            "fields": [
                "main_hero",
                "main_hero_appearance_rate",
                "main_hero_ban_rate",
                "main_hero_channel",
                "main_hero_win_rate",
                "main_heroid",
                "data.sub_hero.hero",
                "data.sub_hero.hero_channel",
                "data.sub_hero.increase_win_rate",
                "data.sub_hero.heroid"
            ]
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero rank: {e}")
            raise
    
    async def fetch_hero_by_position(
        self,
        role: str,
        lane: str,
        page_size: int,
        page_index: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch heroes by role and lane position.
        
        Args:
            role: Hero role
            lane: Hero lane
            page_size: Number of items per page
            page_index: Page index
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero position data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756564")
        
        role_map = {
            "all": [1, 2, 3, 4, 5, 6],
            "tank": [1],
            "fighter": [2],
            "ass": [3],
            "mage": [4],
            "mm": [5],
            "supp": [6],
        }
        
        lane_map = {
            "all": [1, 2, 3, 4, 5],
            "exp": [1],
            "mid": [2],
            "roam": [3],
            "jungle": [4],
            "gold": [5],
        }
        
        payload = {
            "pageSize": page_size,
            "filters": [
                {
                    "field": "<hero.data.sortid>",
                    "operator": "hasAnyOf",
                    "value": role_map.get(role, [1, 2, 3, 4, 5, 6])
                },
                {
                    "field": "<hero.data.roadsort>",
                    "operator": "hasAnyOf",
                    "value": lane_map.get(lane, [1, 2, 3, 4, 5])
                }
            ],
            "sorts": [
                {
                    "data": {"field": "hero_id", "order": "desc"},
                    "type": "sequence"
                }
            ],
            "pageIndex": page_index,
            "fields": [
                "id",
                "hero_id",
                "hero.data.name",
                "hero.data.smallmap",
                "hero.data.sortid",
                "hero.data.roadsort"
            ],
            "object": []
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch heroes by position: {e}")
            raise
    
    async def fetch_hero_detail(
        self,
        hero_id: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch detailed hero information.
        
        Args:
            hero_id: Hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero detail data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756564")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "object": []
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero detail: {e}")
            raise
    
    async def fetch_hero_stats(
        self,
        main_heroid: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero statistics.
        
        Args:
            main_heroid: Main hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero stats data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756567")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "101"},
                {"field": "match_type", "operator": "eq", "value": "1"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero stats: {e}")
            raise
    
    async def fetch_hero_skill_combo(
        self,
        hero_id: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero skill combo information.
        
        Args:
            hero_id: Hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero skill combo data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2674711")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "object": [2684183]
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero skill combo: {e}")
            raise
    
    async def fetch_hero_rate(
        self,
        main_heroid: int,
        past_days: str,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero rate over time.
        
        Args:
            main_heroid: Main hero identifier
            past_days: Time period (7, 15, 30)
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero rate data
            
        Raises:
            RequestException: If request fails
        """
        endpoint_map = {
            "7": self._build_endpoint("2674709"),
            "15": self._build_endpoint("2687909"),
            "30": self._build_endpoint("2690860"),
        }
        
        endpoint = endpoint_map.get(past_days, endpoint_map["7"])
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "8"},
                {"field": "match_type", "operator": "eq", "value": "1"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero rate: {e}")
            raise
    
    async def fetch_hero_relation(
        self,
        hero_id: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero relation information.
        
        Args:
            hero_id: Hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero relation data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756564")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "hero_id", "operator": "eq", "value": hero_id}
            ],
            "sorts": [],
            "pageIndex": 1,
            "fields": ["hero.data.name"],
            "object": []
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero relation: {e}")
            raise
    
    async def fetch_hero_counter(
        self,
        main_heroid: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero counter information.
        
        Args:
            main_heroid: Main hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero counter data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756569")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "match_type", "operator": "eq", "value": "0"},
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "7"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero counter: {e}")
            raise
    
    async def fetch_hero_compatibility(
        self,
        main_heroid: int,
        lang: str = "en"
    ) -> Dict[str, Any]:
        """
        Fetch hero compatibility information.
        
        Args:
            main_heroid: Main hero identifier
            lang: Language code
            
        Returns:
            Dict[str, Any]: Hero compatibility data
            
        Raises:
            RequestException: If request fails
        """
        endpoint = self._build_endpoint("2756569")
        
        payload = {
            "pageSize": 20,
            "filters": [
                {"field": "match_type", "operator": "eq", "value": "1"},
                {"field": "main_heroid", "operator": "eq", "value": main_heroid},
                {"field": "bigrank", "operator": "eq", "value": "7"}
            ],
            "sorts": [],
            "pageIndex": 1
        }
        
        headers = build_mlbb_headers(lang)
        
        try:
            response = self.client.post(endpoint, json_data=payload, headers=headers)
            return response.json()
        except RequestException as e:
            logger.error(f"Failed to fetch hero compatibility: {e}")
            raise


# Singleton instance
_mlbb_service: Optional[MLBBService] = None


def get_mlbb_service() -> MLBBService:
    """
    Get MLBB service singleton instance.
    
    Returns:
        MLBBService: MLBB service instance
    """
    global _mlbb_service
    if _mlbb_service is None:
        _mlbb_service = MLBBService()
    return _mlbb_service
