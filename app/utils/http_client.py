"""
HTTP Client Utilities

This module provides HTTP client functionality with proper error handling.
"""

from typing import Dict, Any, Optional
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from app.core.logging import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """HTTP client wrapper with error handling and logging."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize HTTP client.
        
        Args:
            base_url: Base URL for requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
    
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make POST request.
        
        Args:
            endpoint: API endpoint
            json_data: JSON payload
            headers: Request headers
            **kwargs: Additional request arguments
            
        Returns:
            requests.Response: HTTP response
            
        Raises:
            RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug(f"POST {url}")
            response = self.session.post(
                url,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
            
        except Timeout as e:
            logger.error(f"Request timeout for {url}: {e}")
            raise
        except ConnectionError as e:
            logger.error(f"Connection error for {url}: {e}")
            raise
        except RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            raise
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            headers: Request headers
            **kwargs: Additional request arguments
            
        Returns:
            requests.Response: HTTP response
            
        Raises:
            RequestException: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug(f"GET {url}")
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response
            
        except Timeout as e:
            logger.error(f"Request timeout for {url}: {e}")
            raise
        except ConnectionError as e:
            logger.error(f"Connection error for {url}: {e}")
            raise
        except RequestException as e:
            logger.error(f"Request failed for {url}: {e}")
            raise
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()


def build_mlbb_headers(lang: str = "en") -> Dict[str, str]:
    """
    Build headers for MLBB API requests.
    
    Args:
        lang: Language code (default: "en")
        
    Returns:
        Dict[str, str]: Request headers
    """
    headers = {"Content-Type": "application/json"}
    
    if lang and lang != "en":
        headers["x-lang"] = lang
    
    return headers
